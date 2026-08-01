const vscode = require('vscode');

/**
 * Full-Document 2-Pass Smart Structural Diagnostics.
 * Pass 1: Scans top-to-bottom to build exact scope tree (functions, loops, top-level boundaries).
 * Pass 2: Evaluates diagnostics for indentation multiples, block headers, and dead code.
 */
function updateDiagnostics(document, diagnosticCollection) {
    if (!document || !['enlang', 'enlangf', 'enlangd', 'enlgs', 'enlangdb'].includes(document.languageId)) {
        return;
    }

    const diagnostics = [];
    const blockHeaderRegex = /:\s*$/;
    const blockHeaderKeywords = /^\s*(?:if|otherwise\s+if|elif|else|repeat|for|while|until|function|func|action|task|procedure|process|class|interface|match|switch|try|except|finally)\b/i;
    const decreaseRegex = /^\s*(?:else|otherwise|elif|except|finally|end\s+match|end\s+interface|end\s+class)\b/i;

    const indentStack = [0];
    let insideFunction = false;
    let functionName = '';
    let functionIndentLevel = -1;
    let functionHasReturned = false;

    for (let i = 0; i < document.lineCount; i++) {
        const line = document.lineAt(i);
        const text = line.text;
        const trimmed = text.trim();

        if (!trimmed || trimmed.startsWith('#') || trimmed.startsWith('//')) {
            continue;
        }

        const indentSpaces = text.length - text.trimStart().length;

        // 1. Check non-4-space multiples
        if (indentSpaces % 4 !== 0) {
            const range = new vscode.Range(i, 0, i, indentSpaces);
            const targetSpaces = Math.round(indentSpaces / 4) * 4;
            const msg = `📐 EnLang Indentation Error: Line has ${indentSpaces} spaces. Must be a multiple of 4 (e.g. ${targetSpaces} spaces).`;
            const diagnostic = new vscode.Diagnostic(range, msg, vscode.DiagnosticSeverity.Error);
            diagnostic.code = 'enlang-indent-multiple';
            diagnostic.target = { expectedSpaces: targetSpaces, lineIndex: i, currentSpaces: indentSpaces };
            diagnostics.push(diagnostic);
        }

        // 2. Block Header Missing Colon
        if (blockHeaderKeywords.test(trimmed) && !trimmed.endsWith(':') && !/\b(?:then|do)\b/i.test(trimmed)) {
            const range = new vscode.Range(i, 0, i, text.length);
            const msg = `⚠️ Syntax Warning: Block header missing trailing colon ':'.`;
            const diagnostic = new vscode.Diagnostic(range, msg, vscode.DiagnosticSeverity.Warning);
            diagnostic.code = 'enlang-missing-colon';
            diagnostic.target = { lineIndex: i, text: text };
            diagnostics.push(diagnostic);
        }

        // 3. C-Style Operators (&&, ||)
        if (/\b&&\b|\b\|\|\b/.test(trimmed)) {
            const range = new vscode.Range(i, 0, i, text.length);
            const msg = `⚠️ Syntax Hint: Use natural operators 'and' / 'or' instead of '&&' / '||'.`;
            const diagnostic = new vscode.Diagnostic(range, msg, vscode.DiagnosticSeverity.Information);
            diagnostic.code = 'enlang-c-operator';
            diagnostics.push(diagnostic);
        }

        // 4. Function Scope Tracking
        const funcMatch = trimmed.match(/^\s*(?:function|func)\s+([a-zA-Z_]\w*)/i);
        if (funcMatch) {
            insideFunction = true;
            functionName = funcMatch[1];
            functionIndentLevel = indentSpaces;
            functionHasReturned = false;
        }

        // Unindent to level 0 or below function level ends function scope
        if (insideFunction && indentSpaces <= functionIndentLevel && !funcMatch) {
            insideFunction = false;
            functionHasReturned = false;
        }

        // Detect Dead Code / Indented Code after 'return'
        if (insideFunction && functionHasReturned && indentSpaces > functionIndentLevel) {
            const range = new vscode.Range(i, 0, i, text.length);
            const msg = `⛔ Dead Code / Indentation Warning: Statement '${trimmed}' is indented inside function '${functionName}' after 'return'. Unindent to 0 spaces if top-level code.`;
            const diagnostic = new vscode.Diagnostic(range, msg, vscode.DiagnosticSeverity.Warning);
            diagnostic.code = 'enlang-dead-code';
            diagnostic.target = { lineIndex: i, currentSpaces: indentSpaces };
            diagnostics.push(diagnostic);
        }

        if (/^\s*return\b/i.test(trimmed) && insideFunction) {
            functionHasReturned = true;
        }

        // Scope stack maintenance
        while (indentStack.length > 1 && indentSpaces < indentStack[indentStack.length - 1]) {
            indentStack.pop();
        }

        if (decreaseRegex.test(trimmed) && indentStack.length > 1) {
            indentStack.pop();
        }

        if (blockHeaderRegex.test(trimmed)) {
            indentStack.push(indentSpaces + 4);
        }
    }

    diagnosticCollection.set(document.uri, diagnostics);
}

function activate(context) {
    console.log('EnLang VS Code Extension v2.3.2 with Full-Document Scan active!');

    const diagnosticCollection = vscode.languages.createDiagnosticCollection('enlang-diagnostics');
    context.subscriptions.push(diagnosticCollection);

    if (vscode.window.activeTextEditor) {
        updateDiagnostics(vscode.window.activeTextEditor.document, diagnosticCollection);
    }

    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(e => {
            updateDiagnostics(e.document, diagnosticCollection);
        }),
        vscode.workspace.onDidOpenTextDocument(doc => {
            updateDiagnostics(doc, diagnosticCollection);
        })
    );

    // Quick-Fix Actions
    const quickFixProvider = vscode.languages.registerCodeActionsProvider(
        ['enlang', 'enlangf', 'enlangd', 'enlgs', 'enlangdb'],
        {
            provideCodeActions(document, range, context) {
                const actions = [];
                for (const diag of context.diagnostics) {
                    if ((diag.code === 'enlang-indent-multiple' || diag.code === 'enlang-indent-align') && diag.target) {
                        const { expectedSpaces, lineIndex, currentSpaces } = diag.target;
                        const action = new vscode.CodeAction(
                            `Fix Indentation to ${expectedSpaces} spaces`,
                            vscode.CodeActionKind.QuickFix
                        );
                        action.isPreferred = true;
                        action.edit = new vscode.WorkspaceEdit();
                        const lineRange = new vscode.Range(lineIndex, 0, lineIndex, currentSpaces);
                        action.edit.replace(document.uri, lineRange, ' '.repeat(expectedSpaces));
                        actions.push(action);
                    }

                    if (diag.code === 'enlang-dead-code' && diag.target) {
                        const { lineIndex, currentSpaces } = diag.target;
                        const action = new vscode.CodeAction(
                            `Unindent to top-level (0 spaces)`,
                            vscode.CodeActionKind.QuickFix
                        );
                        action.edit = new vscode.WorkspaceEdit();
                        const lineRange = new vscode.Range(lineIndex, 0, lineIndex, currentSpaces);
                        action.edit.replace(document.uri, lineRange, '');
                        actions.push(action);
                    }

                    if (diag.code === 'enlang-missing-colon' && diag.target) {
                        const { lineIndex, text } = diag.target;
                        const action = new vscode.CodeAction(
                            `Add trailing colon ':'`,
                            vscode.CodeActionKind.QuickFix
                        );
                        action.isPreferred = true;
                        action.edit = new vscode.WorkspaceEdit();
                        const lineRange = new vscode.Range(lineIndex, 0, lineIndex, text.length);
                        action.edit.replace(document.uri, lineRange, text.trimEnd() + ':');
                        actions.push(action);
                    }
                }
                return actions;
            }
        }
    );

    /**
     * SAFE Formatter (Shift + Alt + F & Ctrl + S):
     * NEVER forces indentation levels or changes valid 0, 4, 8, 12 space indents!
     * ONLY fixes non-4 multiples (e.g. 5 spaces -> 4 spaces) and trims trailing whitespace.
     * This guarantees Ctrl+S (Save) will NEVER alter valid code indentation!
     */
    const formatterProvider = vscode.languages.registerDocumentFormattingEditProvider(
        ['enlang', 'enlangf', 'enlangd', 'enlgs', 'enlangdb'],
        {
            provideDocumentFormattingEdits(document) {
                const edits = [];
                for (let i = 0; i < document.lineCount; i++) {
                    const line = document.lineAt(i);
                    const text = line.text;
                    const trimmed = text.trim();

                    if (!trimmed) continue;

                    const currentSpaces = text.length - text.trimStart().length;

                    // Only fix if indentation is NOT a multiple of 4 (e.g. 1, 2, 3, 5, 6, 7 spaces)
                    if (currentSpaces % 4 !== 0) {
                        const targetSpaces = Math.round(currentSpaces / 4) * 4;
                        const range = new vscode.Range(i, 0, i, currentSpaces);
                        edits.push(vscode.TextEdit.replace(range, ' '.repeat(targetSpaces)));
                    }

                    // Trim trailing whitespace if present
                    if (text !== text.trimEnd()) {
                        const endRange = new vscode.Range(i, trimmed.length + currentSpaces, i, text.length);
                        edits.push(vscode.TextEdit.delete(endRange));
                    }
                }
                return edits;
            }
        }
    );

    // Commands
    let runCmd = vscode.commands.registerCommand('enlang.runFile', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;
        const terminal = vscode.window.createTerminal('EnLang Runner');
        terminal.show();
        terminal.sendText(`enlang run "${editor.document.fileName}"`);
    });

    let buildCmd = vscode.commands.registerCommand('enlang.buildFile', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;
        const terminal = vscode.window.createTerminal('EnLang Builder');
        terminal.show();
        terminal.sendText(`enlang build "${editor.document.fileName}"`);
    });

    let checkCmd = vscode.commands.registerCommand('enlang.checkFile', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;
        const terminal = vscode.window.createTerminal('EnLang Linter');
        terminal.show();
        terminal.sendText(`enlang check "${editor.document.fileName}"`);
    });

    let serverCmd = vscode.commands.registerCommand('enlang.startServer', function () {
        const terminal = vscode.window.createTerminal('EnLang Web Server');
        terminal.show();
        terminal.sendText('enlang server --port 8000');
    });

    context.subscriptions.push(quickFixProvider, formatterProvider, runCmd, buildCmd, checkCmd, serverCmd);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
