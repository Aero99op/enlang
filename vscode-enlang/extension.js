const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

/**
 * Calculates correct indentation and returns diagnostics for invalid indentation.
 */
function updateIndentationDiagnostics(document, diagnosticCollection) {
    if (!document || !['enlang', 'enlangf', 'enlangd', 'enlgs', 'enlangdb'].includes(document.languageId)) {
        return;
    }

    const diagnostics = [];
    let expectedIndentLevel = 0;
    const blockHeaderRegex = /:\s*$/;
    const decreaseRegex = /^\s*(?:else|otherwise|elif|except|finally|end\s+match|end\s+interface|end\s+class)\b/i;

    for (let i = 0; i < document.lineCount; i++) {
        const line = document.lineAt(i);
        const text = line.text;
        const trimmed = text.trim();

        if (!trimmed || trimmed.startsWith('#') || trimmed.startsWith('//')) {
            continue;
        }

        if (decreaseRegex.test(trimmed) && expectedIndentLevel > 0) {
            expectedIndentLevel = Math.max(0, expectedIndentLevel - 1);
        }

        const indentSpaces = text.length - text.trimStart().length;
        const expectedSpaces = expectedIndentLevel * 4;

        if (indentSpaces !== expectedSpaces && indentSpaces % 4 !== 0) {
            const range = new vscode.Range(i, 0, i, indentSpaces);
            const needed = expectedSpaces - indentSpaces;
            let actionHint = needed > 0 ? `Add ${needed} spaces` : `Remove ${Math.abs(needed)} spaces`;
            const msg = `💡 EnLang Indentation Helper: Line has ${indentSpaces} spaces. Expected ${expectedSpaces} spaces (4-space multiples). [${actionHint}]`;
            
            const diagnostic = new vscode.Diagnostic(range, msg, vscode.DiagnosticSeverity.Warning);
            diagnostic.code = 'enlang-indent';
            diagnostic.target = { expectedSpaces, lineIndex: i, currentSpaces: indentSpaces };
            diagnostics.push(diagnostic);
        }

        if (blockHeaderRegex.test(trimmed)) {
            expectedIndentLevel++;
        }
    }

    diagnosticCollection.set(document.uri, diagnostics);
}

function activate(context) {
    console.log('EnLang VS Code Extension with Smart Indentation Helper is active!');

    const diagnosticCollection = vscode.languages.createDiagnosticCollection('enlang-indentation');
    context.subscriptions.push(diagnosticCollection);

    // Real-time diagnostics on open and edit
    if (vscode.window.activeTextEditor) {
        updateIndentationDiagnostics(vscode.window.activeTextEditor.document, diagnosticCollection);
    }

    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(e => {
            updateIndentationDiagnostics(e.document, diagnosticCollection);
        }),
        vscode.workspace.onDidOpenTextDocument(doc => {
            updateIndentationDiagnostics(doc, diagnosticCollection);
        })
    );

    // Quick-Fix Provider for Indentation Warning
    const quickFixProvider = vscode.languages.registerCodeActionsProvider(
        ['enlang', 'enlangf', 'enlangd', 'enlgs', 'enlangdb'],
        {
            provideCodeActions(document, range, context) {
                const actions = [];
                for (const diag of context.diagnostics) {
                    if (diag.code === 'enlang-indent' && diag.target) {
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
                }
                return actions;
            }
        }
    );

    // Document Formatting Provider (Format Document: Shift + Alt + F)
    const formatterProvider = vscode.languages.registerDocumentFormattingEditProvider(
        ['enlang', 'enlangf', 'enlangd', 'enlgs', 'enlangdb'],
        {
            provideDocumentFormattingEdits(document) {
                const edits = [];
                let expectedIndentLevel = 0;
                const blockHeaderRegex = /:\s*$/;
                const decreaseRegex = /^\s*(?:else|otherwise|elif|except|finally|end\s+match|end\s+interface|end\s+class)\b/i;

                for (let i = 0; i < document.lineCount; i++) {
                    const line = document.lineAt(i);
                    const text = line.text;
                    const trimmed = text.trim();

                    if (!trimmed || trimmed.startsWith('#') || trimmed.startsWith('//')) {
                        continue;
                    }

                    if (decreaseRegex.test(trimmed) && expectedIndentLevel > 0) {
                        expectedIndentLevel = Math.max(0, expectedIndentLevel - 1);
                    }

                    const currentSpaces = text.length - text.trimStart().length;
                    const targetSpaces = expectedIndentLevel * 4;

                    if (currentSpaces !== targetSpaces) {
                        const range = new vscode.Range(i, 0, i, currentSpaces);
                        edits.push(vscode.TextEdit.replace(range, ' '.repeat(targetSpaces)));
                    }

                    if (blockHeaderRegex.test(trimmed)) {
                        expectedIndentLevel++;
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
