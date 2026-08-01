const vscode = require('vscode');

/**
 * Calculates correct indentation, block structure, and syntax diagnostics in real-time.
 */
function updateDiagnostics(document, diagnosticCollection) {
    if (!document || !['enlang', 'enlangf', 'enlangd', 'enlgs', 'enlangdb'].includes(document.languageId)) {
        return;
    }

    const diagnostics = [];
    const indentStack = [0];
    let insideFunction = false;
    let functionName = '';
    let functionIndentLevel = -1;
    let functionHasReturned = false;

    const blockHeaderRegex = /:\s*$/;
    const decreaseRegex = /^\s*(?:else|otherwise|elif|except|finally|end\s+match|end\s+interface|end\s+class)\b/i;

    for (let i = 0; i < document.lineCount; i++) {
        const line = document.lineAt(i);
        const text = line.text;
        const trimmed = text.trim();

        if (!trimmed || trimmed.startsWith('#') || trimmed.startsWith('//')) {
            continue;
        }

        const indentSpaces = text.length - text.trimStart().length;

        // 1. 4-Space Multiple Check
        if (indentSpaces % 4 !== 0) {
            const range = new vscode.Range(i, 0, i, indentSpaces);
            const targetSpaces = Math.round(indentSpaces / 4) * 4;
            const msg = `📐 EnLang Indentation Error: Line has ${indentSpaces} spaces. EnLang requires 4-space multiples (e.g. ${targetSpaces} spaces).`;
            const diagnostic = new vscode.Diagnostic(range, msg, vscode.DiagnosticSeverity.Error);
            diagnostic.code = 'enlang-indent-multiple';
            diagnostic.target = { expectedSpaces: targetSpaces, lineIndex: i, currentSpaces: indentSpaces };
            diagnostics.push(diagnostic);
        }

        // 2. Block Header Missing Colon Check
        const blockHeaderKeywords = /^\s*(?:if|otherwise\s+if|elif|else|repeat|for|while|until|function|func|action|task|procedure|process|class|interface|match|switch|try|except|finally)\b/i;
        if (blockHeaderKeywords.test(trimmed) && !trimmed.endsWith(':') && !/\b(?:then|do)\b/i.test(trimmed)) {
            const range = new vscode.Range(i, 0, i, text.length);
            const msg = `⚠️ Syntax Warning: Block header missing trailing colon ':'. Add a colon at the end of the line.`;
            const diagnostic = new vscode.Diagnostic(range, msg, vscode.DiagnosticSeverity.Warning);
            diagnostic.code = 'enlang-missing-colon';
            diagnostic.target = { lineIndex: i, text: text };
            diagnostics.push(diagnostic);
        }

        // 3. C-Style Operator Check (&&, ||)
        if (/\b&&\b|\b\|\|\b/.test(trimmed)) {
            const range = new vscode.Range(i, 0, i, text.length);
            const msg = `⚠️ Syntax Hint: C-style logical operators '&&' / '||' detected. Use natural operators 'and' / 'or'.`;
            const diagnostic = new vscode.Diagnostic(range, msg, vscode.DiagnosticSeverity.Information);
            diagnostic.code = 'enlang-c-operator';
            diagnostics.push(diagnostic);
        }

        // 4. Function & Scope Tracking
        const funcMatch = trimmed.match(/^\s*(?:function|func)\s+([a-zA-Z_]\w*)/i);
        if (funcMatch) {
            insideFunction = true;
            functionName = funcMatch[1];
            functionIndentLevel = indentSpaces;
            functionHasReturned = false;
        }

        // Pop stack levels if current line is un-indented
        while (indentStack.length > 1 && indentSpaces < indentStack[indentStack.length - 1]) {
            indentStack.pop();
        }

        if (insideFunction && indentSpaces <= functionIndentLevel && !funcMatch) {
            insideFunction = false;
            functionHasReturned = false;
        }

        // Detect Dead Code after return inside the same function scope
        if (insideFunction && functionHasReturned && indentSpaces > functionIndentLevel) {
            const range = new vscode.Range(i, 0, i, text.length);
            const msg = `⛔ Dead Code / Indentation Warning: Statement '${trimmed}' is indented inside function '${functionName}' after 'return'. Did you mean to unindent to 0 spaces?`;
            const diagnostic = new vscode.Diagnostic(range, msg, vscode.DiagnosticSeverity.Warning);
            diagnostic.code = 'enlang-dead-code';
            diagnostic.target = { lineIndex: i, currentSpaces: indentSpaces };
            diagnostics.push(diagnostic);
        }

        if (/^\s*return\b/i.test(trimmed) && insideFunction) {
            functionHasReturned = true;
        }

        if (blockHeaderRegex.test(trimmed)) {
            indentStack.push(indentSpaces + 4);
        }
    }

    diagnosticCollection.set(document.uri, diagnostics);
}

function activate(context) {
    console.log('EnLang VS Code Extension active!');

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

    // Quick-Fix Actions for Indentation & Colons
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

    // Smart Auto-Formatter (Shift + Alt + F & Format on Save)
    // Respects user un-indentation & normalizes non-4 multiples safely
    const formatterProvider = vscode.languages.registerDocumentFormattingEditProvider(
        ['enlang', 'enlangf', 'enlangd', 'enlgs', 'enlangdb'],
        {
            provideDocumentFormattingEdits(document) {
                const edits = [];
                let indentLevelStack = [0];
                const blockHeaderRegex = /:\s*$/;
                const decreaseRegex = /^\s*(?:else|otherwise|elif|except|finally|end\s+match|end\s+interface|end\s+class)\b/i;

                for (let i = 0; i < document.lineCount; i++) {
                    const line = document.lineAt(i);
                    const text = line.text;
                    const trimmed = text.trim();

                    if (!trimmed || trimmed.startsWith('#') || trimmed.startsWith('//')) {
                        continue;
                    }

                    const currentSpaces = text.length - text.trimStart().length;

                    // Pop stack if line is unindented by user
                    while (indentLevelStack.length > 1 && currentSpaces < indentLevelStack[indentLevelStack.length - 1]) {
                        indentLevelStack.pop();
                    }

                    // Handle dedent keywords (else, elif, etc.)
                    if (decreaseRegex.test(trimmed) && indentLevelStack.length > 1) {
                        indentLevelStack.pop();
                    }

                    // Round current spaces to nearest 4-space multiple while respecting scope
                    let targetSpaces = Math.round(currentSpaces / 4) * 4;

                    if (currentSpaces !== targetSpaces) {
                        const range = new vscode.Range(i, 0, i, currentSpaces);
                        edits.push(vscode.TextEdit.replace(range, ' '.repeat(targetSpaces)));
                    }

                    if (blockHeaderRegex.test(trimmed)) {
                        indentLevelStack.push(targetSpaces + 4);
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
