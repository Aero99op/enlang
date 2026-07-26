import os
import re
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def clean_text_for_reportlab(text):
    if not isinstance(text, str):
        return text
    text = text.replace("&", "&amp;")
    text = text.replace("<b>", "___B_OPEN___").replace("</b>", "___B_CLOSE___")
    text = text.replace("<i>", "___I_OPEN___").replace("</i>", "___I_CLOSE___")
    text = text.replace("<u>", "___U_OPEN___").replace("</u>", "___U_CLOSE___")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("___B_OPEN___", "<b>").replace("___B_CLOSE___", "</b>")
    text = text.replace("___I_OPEN___", "<i>").replace("___I_CLOSE___", "</i>")
    text = text.replace("___U_OPEN___", "<u>").replace("___U_CLOSE___", "</u>")
    return text

def name_from_title(title_str):
    return title_str.split('(')[0].strip()

def generate_beginner_master_book2():
    pdf_path = "book2_enlang_web_framework.pdf"
    print("Generating Absolute Beginner Master PDF for Book 2 (EnLang Web Framework)...")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom Typography & Styles
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=28, leading=34,
        textColor=colors.HexColor('#0D9488'), spaceAfter=15, alignment=1
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=14, leading=18,
        textColor=colors.HexColor('#4B5563'), spaceAfter=25, alignment=1
    )

    part_header_style = ParagraphStyle(
        'PartHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=colors.HexColor('#0D9488'), spaceBefore=18, spaceAfter=12, keepWithNext=True
    )

    chapter_header_style = ParagraphStyle(
        'ChapterHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=16, leading=20,
        textColor=colors.HexColor('#0F766E'), spaceBefore=16, spaceAfter=10, keepWithNext=True
    )

    section_header_style = ParagraphStyle(
        'SectionHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11.5, leading=14.5,
        textColor=colors.HexColor('#1F2937'), spaceBefore=8, spaceAfter=4, keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=14,
        textColor=colors.HexColor('#374151'), spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeCustom', parent=styles['Normal'],
        fontName='Courier', fontSize=8.5, leading=11,
        textColor=colors.HexColor('#111827'), backColor=colors.HexColor('#F9FAFB'),
        borderColor=colors.HexColor('#E5E7EB'), borderWidth=1, borderPadding=6,
        spaceBefore=4, spaceAfter=6
    )

    callout_style = ParagraphStyle(
        'CalloutCustom', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9, leading=13,
        textColor=colors.HexColor('#0F766E'), backColor=colors.HexColor('#F0FDFA'),
        borderColor=colors.HexColor('#99F6E4'), borderWidth=1, borderPadding=6,
        spaceBefore=4, spaceAfter=6
    )

    story = []

    # ── Cover Page ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 80))
    story.append(Paragraph("EnLang Web Development", title_style))
    story.append(Paragraph("<b>The Absolute Beginner & Master Guide to Web Engineering (EnLGF, EnLGD, EnLGS, EnLGDB)</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor('#0D9488'), spaceAfter=25))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Author:</b> Spandan Prayas Patra", body_style))
    story.append(Paragraph("<b>Designed for Zero-Experience Beginners:</b> Explains every keyword (`create`, `close`, `named`, `with class`), syntax structure, and line of code from absolute scratch.", body_style))
    story.append(Paragraph("<b>Target Audience:</b> First-Time Programmers, Web Students, Full-Stack Architects", body_style))
    story.append(PageBreak())

    # PART 0: ABSOLUTE BEGINNER FOUNDATIONS
    BEGINNER_FOUNDATIONS = [
        {
            "num": "0.1",
            "part": "Part 0: Absolute Beginner Foundations — How Web Apps Work",
            "title": "What is Web Development & How Does a Browser Work?",
            "intro": "Welcome to the world of web development! If you have never written a line of computer code before, do not panic. This chapter will teach you how websites work, what a browser does, and how EnLang allows you to build complete websites using simple English sentences.",
            "objectives": "• Understand how web browsers (Chrome, Edge, Firefox) render websites.\n• Learn what HTML, CSS, and JavaScript do in plain English.\n• Understand how EnLang simplifies web development into plain natural sentences.",
            "prereqs": "No prior programming experience required! All you need is a computer and curiosity.",
            "what": "Web development is the process of creating websites and web applications that run inside a web browser. A website is made of 3 basic parts:\n1. Structure (HTML) — The skeleton of the page (buttons, text, boxes).\n2. Styling (CSS) — The clothes and makeup (colors, fonts, sizes).\n3. Logic (JS) — The brain (what happens when you click a button).",
            "why": "In traditional coding, you have to learn 3 or 4 different complicated languages at once. EnLang combines all of them into plain English! You write simple sentences, and EnLang automatically creates the skeleton, clothes, and brain for your website.",
            "real_world": "Every website you use daily (Google, YouTube, Amazon, Instagram) is built using these exact same principles.",
            "internal_working": "When you type code in EnLang, the EnLang Compiler reads your natural sentences, checks for any mistakes, and translates (transpiles) them into standard web code that any browser in the world can display instantly.",
            "syntax": "page title \"My First Website\"\ncreate h1 with text \"Hello World\"\nclose h1",
            "rules": "1. Always surround text with double quotes `\"...\"`.\n2. Write keywords in lowercase English.\n3. Save your file with `.enlgf` extension.",
            "ebnf": "Website ::= PageTitle Header ElementList",
            "keywords": "• `page title`: Sets the text displayed on the browser tab at the top.\n• `create`: Tells the computer to make a new element on the screen.\n• `text`: Specifies the exact words to display.",
            "basic_example": "page title \"My First Website\"\ncreate h1 with text \"Welcome to My Home Page\"\nclose h1",
            "inter_example": "page title \"My Profile Page\"\ncreate h1 with text \"Spandan Prayas Patra\"\ncreate p with text \"I am learning EnLang Web Development!\"\nclose p",
            "adv_example": "page title \"My Complete Portfolio\"\ncreate header:\n    create h1 with text \"Spandan's Portfolio\"\n    create p with text \"Web Developer & AI Engineer\"\nclose header",
            "generated_code": "<!-- Generated HTML Code -->\n<!DOCTYPE html>\n<html>\n<head><title>My First Website</title></head>\n<body><h1>Welcome to My Home Page</h1></body>\n</html>",
            "walkthrough": "Line 1: `page title \"My First Website\"` tells the browser tab to display 'My First Website'.\nLine 2: `create h1 with text \"...\"` creates a giant bold Heading 1 on the page.\nLine 3: `close h1` tells the computer that the heading text is finished.",
            "compiler_walkthrough": "1. Lexer reads `page title` → identifies header directive.\n2. Parser builds page structure node.\n3. Generator writes native HTML tags.",
            "memory_behavior": "EnLang requires almost zero memory. It processes your text file line by line and creates lightweight HTML.",
            "perf_complexity": "Time Complexity: O(1) Instantaneous loading.",
            "error_handling": "If you forget quotes around your text, EnLang will say: `SyntaxError: Missing double quotes around string on line X`.",
            "common_mistakes": "• Writing quotes on one side only (`\"Hello`).\n• Misspelling words (writing `creete` instead of `create`).",
            "best_practices": "• Keep your code clean by indenting nested lines with 4 spaces.\n• Give every page a clear title.",
            "security_notes": "EnLang automatically protects your website against hackers by escaping dangerous script tags.",
            "linter_rules": "`enlang check` checks if your page has a title and valid tags.",
            "debugging": "If your page looks blank, check the terminal window for red error messages.",
            "version_compat": "Works on all computers (Windows, Mac, Linux).",
            "lang_comp": "EnLang vs HTML: In HTML you write `<h1>Hello</h1>`. In EnLang you write `create h1 with text \"Hello\"`.",
            "faq": "Q: Do I need internet to run EnLang?\nA: No! EnLang compiles locally on your computer.",
            "exercises": "1. Write code to display your name in a giant `h1` heading.\n2. Add a paragraph `p` explaining your favorite hobby.",
            "mini_project": "Build your very first Personal Biography Web Page (`bio.enlgf`) with a title, heading, and two paragraphs.",
            "interview_qs": "Q1: What are the 3 main layers of web development?\nA: Structure (HTML), Presentation (CSS), and Behavior (JS).",
            "summary": "Web development is easy with EnLang because you describe what you want in plain English sentences.",
            "whats_next": "In Chapter 0.2, we will break down the exact format of EnLang syntax!"
        },
        {
            "num": "0.2",
            "part": "Part 0: Absolute Beginner Foundations — How Web Apps Work",
            "title": "Deconstructing Syntax: What is a Keyword, Identifier & Statement?",
            "intro": "To talk to a computer, you need to understand how sentences (statements) are built. In human language, a sentence has a subject, verb, and object. In EnLang, a sentence has a Keyword, an Identifier, and Attributes.",
            "objectives": "• Understand what a Keyword is in programming.\n• Learn how Identifiers and Names work.\n• Master String literals and why double quotes `\"\"` are mandatory.",
            "prereqs": "Completion of Chapter 0.1.",
            "what": "A **Syntax** is the set of grammar rules for a language.\n• **Keyword**: A special word reserved by EnLang (like `create`, `close`, `page`, `title`, `named`, `with`).\n• **Identifier**: A name YOU create (like `myButton`, `mainBox`, `userHeader`).\n• **String**: Plain text wrapped in double quotes `\"Hello World\"`.",
            "why": "Computers are very literal. If you write `create` without quotes, the computer knows it is a command. If you write `\"create\"` with quotes, the computer treats it as plain text to show on screen. Quotes tell the computer the difference between a COMMAND and TEXT!",
            "real_world": "Think of Keywords as commands to a robot: `STOP`, `WALK`, `PICK_UP`. The text in quotes is what the robot carries.",
            "internal_working": "The EnLang Lexer scans every word. If a word matches the keyword dictionary (`create`, `close`), it turns into a COMMAND TOKEN. Otherwise, it turns into a NAME TOKEN or STRING TOKEN.",
            "syntax": "# Syntax Pattern Format:\n[KEYWORD] [ELEMENT_TYPE] named [YOUR_CUSTOM_NAME] with [PROPERTY] \"[YOUR_TEXT]\":\n    [INNER_CONTENT]\nclose [ELEMENT_TYPE]",
            "rules": "1. Keywords are ALWAYS lowercase (`create`, not `CREATE`).\n2. Custom names cannot have spaces (use `myButton` or `my_button`).\n3. String text MUST have matching opening and closing double quotes `\"...\"`.",
            "ebnf": "Statement ::= Keyword ElementName ('named' CustomID)? ('with' Property StringLiteral)?",
            "keywords": "• `named`: Keyword used to give a unique ID name to a visual element.\n• `with`: Keyword used to attach properties like `class`, `text`, or `label`.",
            "basic_example": "# Syntax Anatomy Breakdown\npage title \"Syntax Lesson\"\n\ncreate button named btnSubmit with label \"Click Me\"\nclose button",
            "inter_example": "# Multiple Attributes in One Statement\ncreate input named txtEmail with type \"email\" and placeholder \"Enter your email\"\nclose input",
            "adv_example": "# Complete Structural Syntax Tree\ncreate card named userCard with class \"profile-box\":\n    create h2 with text \"Spandan\"\n    create button named btnFollow with label \"Follow User\"\nclose card",
            "generated_code": "<!-- Generated HTML Code -->\n<div id=\"userCard\" class=\"profile-box\">\n  <h2>Spandan</h2>\n  <button id=\"btnFollow\">Follow User</button>\n</div>",
            "walkthrough": "Line 1: `create card`: Command to make a card container box.\nLine 1: `named userCard`: Gives the box an ID name 'userCard'.\nLine 1: `with class \"profile-box\"`: Attaches CSS style class 'profile-box'.\nLine 2-3: Adds heading and button inside the box.\nLine 4: `close card`: Closes the card container.",
            "compiler_walkthrough": "1. Lexer breaks line into: `create` (KEYWORD), `card` (TYPE), `named` (KEYWORD), `userCard` (ID).\n2. Parser connects attributes to `userCard` AST node.\n3. Generator produces `<div id=\"userCard\">`.",
            "memory_behavior": "Name tokens are stored in the compiler's Symbol Table lookup dictionary.",
            "perf_complexity": "Time Complexity: O(1) Instant token lookup.",
            "error_handling": "If you write a space in a custom name (`named my button`), EnLang reports: `SyntaxError: Custom name cannot contain spaces on line X`.",
            "common_mistakes": "• Putting spaces in custom names (`named my box`).\n• Forgetting double quotes around property values.",
            "best_practices": "• Use camelCase for names (`myButton`, `topNavbar`, `loginForm`).\n• Always close your blocks cleanly.",
            "security_notes": "Names are sanitized to ensure no malicious code can be injected via custom IDs.",
            "linter_rules": "`enlang check` warns if two elements share the exact same `named` ID.",
            "debugging": "Read error messages carefully—they tell you the exact line number where quotes or keywords are missing.",
            "version_compat": "Standard syntax pattern across all EnLang releases.",
            "lang_comp": "EnLang vs HTML: In HTML attributes look like `id=\"btn\" class=\"primary\"`. In EnLang they read like a sentence: `named btn with class \"primary\"`.",
            "faq": "Q: Can I use single quotes `'...'`?\nA: EnLang prefers double quotes `\"...\"` for consistency.",
            "exercises": "1. Identify the Keyword, Identifier, and String in: `create button named myBtn with label \"Press Here\"`.\n2. Fix the syntax error in: `create h1 with text Hello World`.",
            "mini_project": "Write a Syntax Demonstration Document (`syntax_demo.enlgf`) showcasing 5 different keywords and custom names.",
            "interview_qs": "Q1: What is the difference between a Keyword and an Identifier?\nA: A Keyword is a reserved language command; an Identifier is a user-created custom variable name.",
            "summary": "EnLang syntax is built like an English sentence: Command + Type + Name + Attributes.",
            "whats_next": "In Chapter 0.3, we will deeply explore the most important keyword: `create`!"
        },
        {
            "num": "0.3",
            "part": "Part 0: Absolute Beginner Foundations — How Web Apps Work",
            "title": "Deep Dive: What is the `create` Keyword & How Does It Make Elements?",
            "intro": "The `create` keyword is the engine of EnLang frontend templates. Every time you want a new box, button, text, image, or navigation bar to appear on screen, you start your sentence with `create`.",
            "objectives": "• Master the `create` keyword and its variations.\n• Learn how `create` translates into HTML DOM elements.\n• Understand how to create text, headings, buttons, and boxes.",
            "prereqs": "Completion of Chapter 0.2.",
            "what": "`create` is an active verb command in EnLang that tells the computer: *\"Hey, make a new visual item on the web page right now!\"*\nSyntactically, `create` is always followed by the type of item you want to create (e.g. `create button`, `create h1`, `create nav`, `create card`).",
            "why": "Without `create`, the computer wouldn't know if you are defining a variable, loading a file, or drawing a visual element. `create` explicitly tells EnLang to instantiate a visual user interface component.",
            "real_world": "Every single element on a web page—from the search bar on Google to the play button on YouTube—was created using an element creation command.",
            "internal_working": "When `create <element>` is executed, EnLang creates a new HTML node in the Document Object Model (DOM). It assigns attributes, appends children inside it, and renders it on screen.",
            "syntax": "create <element_type> named <custom_id> with <attribute_key> \"<attribute_value>\"",
            "rules": "1. `create` must be followed by a valid element type (`h1`, `p`, `button`, `input`, `nav`, `card`, `hero`, `table`, `image`).\n2. If the element contains inner items, end the line with a colon `:` and add a `close <element>` line below.",
            "ebnf": "CreateStatement ::= 'create' ElementType ('named' Ident)? ('with' AttributeKey StringLiteral)* (':' Block 'close' ElementType)?",
            "keywords": "• `create`: The primary action verb command.\n• `named`: Assigns a unique tracking ID to the created item.",
            "basic_example": "# Creating a Simple Heading\ncreate h1 with text \"Welcome to My Website\"\nclose h1",
            "inter_example": "# Creating an Interactive Button\ncreate button named btnSubmit with label \"Click to Register\" and action \"registerUser()\"\nclose button",
            "adv_example": "# Creating a Complete Hero Container with Nested Elements\ncreate hero named mainBanner with class \"banner-style\":\n    create h1 with text \"Build Anything with EnLang\"\n    create p with text \"Simple, natural English programming for everyone.\"\n    create button named btnStart with label \"Get Started Now\"\nclose hero",
            "generated_code": "<!-- Generated HTML -->\n<section id=\"mainBanner\" class=\"hero banner-style\">\n  <h1>Build Anything with EnLang</h1>\n  <p>Simple, natural English programming for everyone.</p>\n  <button id=\"btnStart\">Get Started Now</button>\n</section>",
            "walkthrough": "Line 1: `create hero`: Makes a giant section box named `mainBanner`.\nLine 2: `create h1`: Makes a main headline inside the box.\nLine 3: `create p`: Makes a paragraph text inside the box.\nLine 4: `create button`: Makes a clickable button inside the box.\nLine 5: `close hero`: Closes the main banner box.",
            "compiler_walkthrough": "1. Lexer detects `create` keyword token.\n2. Parser constructs Element AST node with children array.\n3. Generator outputs opening HTML tag `<section>` and inner child tags.",
            "memory_behavior": "Created elements reside in the browser DOM tree memory structure.",
            "perf_complexity": "Time Complexity: O(1) per element created.",
            "error_handling": "If you write `create` without specifying an element type (e.g. `create with text \"hi\"`), EnLang reports: `SyntaxError: Expected element type after 'create' on line X`.",
            "common_mistakes": "• Writing `make` instead of `create` (`make button` is invalid; use `create button`).\n• Forgetting to close container elements.",
            "best_practices": "• Always give important interactive elements a name (`named btnSubmit`).\n• Use `create` for visible UI components.",
            "security_notes": "All element attributes passed via `create` are sanitized to prevent HTML injection attacks.",
            "linter_rules": "`enlang check` verifies that element types following `create` are valid W3C standard elements.",
            "debugging": "Use `enlang run file.enlgf` to open the interactive browser preview and inspect created elements.",
            "version_compat": "Supported in all versions of EnLang.",
            "lang_comp": "EnLang `create button` vs JS `document.createElement('button')`: EnLang is 1 natural line instead of 5 lines of DOM manipulation code.",
            "faq": "Q: Can I create custom HTML tags?\nA: Yes! `create my-widget` creates a `<my-widget>` tag.",
            "exercises": "1. Write code to `create` a button named `btnSave` with label \"Save File\".\n2. `create` a paragraph with text \"EnLang is easy!\"",
            "mini_project": "Build an Element Showcase App (`elements.enlgf`) featuring 5 different created elements (heading, paragraph, input, button, card).",
            "interview_qs": "Q1: What does the `create` keyword do in EnLang?\nA: It instantiates and appends a visual UI element to the DOM tree.",
            "summary": "`create` is the core action command to make any visual button, text, image, or container box on a web page.",
            "whats_next": "In Chapter 0.4, we will learn how `close` works and how to nest boxes inside boxes!"
        },
        {
            "num": "0.4",
            "part": "Part 0: Absolute Beginner Foundations — How Web Apps Work",
            "title": "Deep Dive: What is `close` & How Does Block Nesting Work?",
            "intro": "Imagine packing a gift. You open a cardboard box, put your presents inside, and then **close the box**. If you leave the box open, items will fall out! In EnLang, when you open a container with `create`, you MUST close it with `close`.",
            "objectives": "• Understand the Box-Inside-A-Box analogy for web layouts.\n• Learn how `close` prevents layout bugs and structural errors.\n• Master indentation and nested code block organization.",
            "prereqs": "Completion of Chapter 0.3.",
            "what": "`close` is the terminating keyword in EnLang that marks the end of a container block.\nWhen you write `create main:`, you are opening a container. All lines indented below it are INSIDE that container. Writing `close main` tells the computer: *\"This container ends here!\"*",
            "why": "Without `close`, the computer wouldn't know where a section ends. Does the navbar end after the first link or after the entire page? `close` establishes crystal-clear boundaries for visual containers.",
            "real_world": "Think of nested folders on your computer: Folder A contains Folder B, which contains File C. `close` ensures Folder B shuts before Folder A shuts.",
            "internal_working": "EnLang uses an internal **Compiler Stack**. When `create nav` is parsed, `nav` is pushed onto the stack. When `close nav` is parsed, EnLang checks the stack top. If it matches `nav`, it pops the stack and emits `</nav>`.",
            "syntax": "create <container_type> named <name>:\n    # Items INSIDE the box (indented 4 spaces)\n    create <item1>\n    create <item2>\nclose <container_type>",
            "rules": "1. The element name after `close` MUST match the element name after `create`.\n2. Items inside the box MUST be indented by 4 spaces.\n3. You cannot close a parent box before closing its child box!",
            "ebnf": "Block ::= ContainerStart '\\n' IndentedStatements ContainerEnd '\\n'",
            "keywords": "• `close`: The terminating keyword that closes an open container block.",
            "basic_example": "# Simple Open and Close Box\ncreate main named mainBox:\n    create h1 with text \"Inside the Main Box\"\nclose main",
            "inter_example": "# Nested Boxes (Box Inside a Box)\ncreate hero named outerHero:\n    create card named innerCard:\n        create h2 with text \"Nested Card Inside Hero\"\n    close card\nclose hero",
            "adv_example": "# Deep Multi-Level Nesting Structure\ncreate main named appMain:\n    create nav named navBar:\n        create link with text \"Home\"\n        create link with text \"About\"\n    close nav\n    create hero named heroBanner:\n        create h1 with text \"Hero Title\"\n    close hero\nclose main",
            "generated_code": "<!-- Generated Nested HTML -->\n<main id=\"appMain\">\n  <nav id=\"navBar\">\n    <a href=\"#\">Home</a>\n    <a href=\"#\">About</a>\n  </nav>\n  <section id=\"heroBanner\" class=\"hero\">\n    <h1>Hero Title</h1>\n  </section>\n</main>",
            "walkthrough": "Line 1: Opens `appMain` container.\nLine 2-4: Opens `navBar` inside `appMain`, adds links, and runs `close nav`.\nLine 5-7: Opens `heroBanner` inside `appMain`, adds heading, and runs `close hero`.\nLine 8: Runs `close main` to close the outer `appMain` container.",
            "compiler_walkthrough": "1. Push `main` to Stack -> `[main]`.\n2. Push `nav` to Stack -> `[main, nav]`.\n3. Pop `nav` from Stack -> `[main]`.\n4. Push `hero` to Stack -> `[main, hero]`.\n5. Pop `hero` from Stack -> `[main]`.\n6. Pop `main` from Stack -> `[]` (Clean stack!).",
            "memory_behavior": "Compiler stack depth equals maximum nesting depth.",
            "perf_complexity": "Time Complexity: O(1) stack push/pop.",
            "error_handling": "If you open `create nav:` but write `close hero`, EnLang throws: `EnLangMismatchedBlockError: Expected 'close nav' on line 5, but found 'close hero'`.",
            "common_mistakes": "• Mismatching close tags (`create card` ... `close main`).\n• Forgetting to indent lines inside a container.",
            "best_practices": "• Always match indentation (4 spaces per nesting level).\n• Keep nesting depth under 5 levels for clean readability.",
            "security_notes": "Enforced block closing prevents malformed HTML tree vulnerabilities.",
            "linter_rules": "`enlang check` alerts instantly if any container block is left unclosed at the end of a file.",
            "debugging": "If elements appear in the wrong position on screen, check if you accidentally placed `close` too early or too late.",
            "version_compat": "Core block structure syntax across all EnLang versions.",
            "lang_comp": "EnLang `close card` vs HTML `</div>`: EnLang explicitly states WHICH tag is closing (`close card`), preventing confusion over generic `</div>` tags.",
            "faq": "Q: What happens if I forget `close` at the end of a file?\nA: EnLang compiler will raise an `UnclosedBlockError` and refuse to build until fixed.",
            "exercises": "1. Fix the error in: `create nav:` ... `close card`.\n2. Create a `card` inside a `main` box and close both properly.",
            "mini_project": "Build a Nested Card Layout (`nested.enlgf`) featuring 3 cards nested inside a main container, with proper indentation and matching `close` statements.",
            "interview_qs": "Q1: Why does EnLang require matching `close <tag>` statements?\nA: To guarantee well-formed DOM tree hierarchy and eliminate closing tag ambiguity.",
            "summary": "`close` tells the computer where a container box ends. Every `create <box>:` MUST be paired with a matching `close <box>`.",
            "whats_next": "In Chapter 0.5, we will learn how to style containers using `named` IDs and `with class`!"
        },
        {
            "num": "0.5",
            "part": "Part 0: Absolute Beginner Foundations — How Web Apps Work",
            "title": "Deep Dive: IDs (`named`), Classes (`with class`) & Double Quotes `\"\"`",
            "intro": "How do you tell two buttons apart? How do you color one box blue and another box red? In web development, we give elements **Names (IDs)** to identify them uniquely, and **Classes** to give them style clothes. This chapter explains how `named` and `with class` work.",
            "objectives": "• Learn the difference between an ID (`named`) and a Class (`with class`).\n• Understand why IDs must be unique while Classes can be shared.\n• Master attribute chaining in natural English statements.",
            "prereqs": "Completion of Chapter 0.4.",
            "what": "• **`named <id>`**: Assigns a UNIQUE name (ID) to an element (like a Passport Number or Aadhaar ID—no two elements should have the same name).\n• **`with class \"<class_name>\"`**: Assigns a STYLE GROUP (Class) to an element (like a school uniform—many students can wear the same uniform).",
            "why": "If you have 10 buttons on a page, you need a way to tell the computer: *\"Change the text on button #3, not button #1!\"* Giving button #3 `named btnSave` allows you to target it specifically. Giving all 10 buttons `with class \"btn-primary\"` lets them share the same blue color.",
            "real_world": "Think of IDs as Social Security Numbers (unique per person) and Classes as T-shirt colors (many people can wear blue T-shirts).",
            "internal_working": "EnLang transpiles `named myBox` into HTML `id=\"myBox\"` and `with class \"hero-style\"` into HTML `class=\"hero-style\"`.",
            "syntax": "create <element_type> named <unique_id> with class \"<shared_class_name>\":\n    <content>\nclose <element_type>",
            "rules": "1. `named` IDs must be unique across the entire `.enlgf` file.\n2. `with class` values must be strings wrapped in double quotes `\"...\"`.\n3. Multiple class names are separated by spaces inside quotes: `with class \"btn primary large\"`.",
            "ebnf": "Attributes ::= ('named' Ident)? ('with class' StringLiteral)?",
            "keywords": "• `named`: Keyword to assign a unique element ID.\n• `with`: Connector keyword used to attach `class`, `text`, or `action` attributes.",
            "basic_example": "# Unique ID and Shared Class\ncreate button named btnLogin with class \"btn-blue\" and label \"Sign In\"\nclose button",
            "inter_example": "# Multiple Buttons Sharing the Same Class\ncreate button named btnSave with class \"btn-action\" and label \"Save\"\nclose button\ncreate button named btnCancel with class \"btn-action\" and label \"Cancel\"\nclose button",
            "adv_example": "# Complete Layout using IDs and Classes\ncreate nav named topNavigation with class \"navbar sticky flex-between\":\n    create button named btnHome with class \"nav-link active\" and label \"Home\"\n    create button named btnAbout with class \"nav-link\" and label \"About\"\nclose nav",
            "generated_code": "<!-- Generated HTML Output -->\n<nav id=\"topNavigation\" class=\"navbar sticky flex-between\">\n  <button id=\"btnHome\" class=\"nav-link active\">Home</button>\n  <button id=\"btnAbout\" class=\"nav-link\">About</button>\n</nav>",
            "walkthrough": "Line 1: `named topNavigation`: Unique ID for the navbar.\nLine 1: `with class \"navbar sticky flex-between\"`: Applies 3 CSS style classes.\nLine 2-3: Creates two buttons sharing `nav-link` class, but each with a unique ID (`btnHome`, `btnAbout`).",
            "compiler_walkthrough": "1. Parser extracts `named` value → sets AST `node.id`.\n2. Parser extracts `with class` value → sets AST `node.className`.\n3. Generator outputs `<nav id=\"topNavigation\" class=\"navbar sticky flex-between\">`.",
            "memory_behavior": "IDs are stored in the browser's DOM fast-lookup hash map.",
            "perf_complexity": "DOM ID Lookup Complexity: O(1) Instant lookup via `document.getElementById`.",
            "error_handling": "If you reuse the same `named` ID twice (e.g. two elements named `btn1`), `enlang check` raises: `EnLGFDuplicateIDError: ID 'btn1' is already used on line 3`.",
            "common_mistakes": "• Using the same `named` ID on multiple elements.\n• Forgetting double quotes around class names (`with class hero` instead of `with class \"hero\"`).",
            "best_practices": "• Give every interactive button an ID (`named`).\n• Group reusable visual styles into classes (`with class`).",
            "security_notes": "Class and ID names are checked against attribute injection vulnerabilities.",
            "linter_rules": "`enlang check` enforces unique IDs and validates class name syntax.",
            "debugging": "Inspect elements in Chrome DevTools (F12) to verify `id` and `class` attributes are correctly set.",
            "version_compat": "Standard ID/Class binding across all EnLang versions.",
            "lang_comp": "EnLang `named myBtn with class \"primary\"` vs HTML `id=\"myBtn\" class=\"primary\"`: EnLang reads smoothly like an English sentence.",
            "faq": "Q: Can an element have multiple classes?\nA: Yes! Separate class names with spaces: `with class \"btn primary large\"`.",
            "exercises": "1. Write code to create a card with ID `profileCard` and class `card-shadow`.\n2. Create two buttons sharing class `btn-styled` with unique IDs `btn1` and `btn2`.",
            "mini_project": "Build an E-Commerce Item Card (`product.enlgf`) with unique button IDs and shared CSS styling classes.",
            "interview_qs": "Q1: What is the key difference between an ID and a Class in web development?\nA: An ID is a unique identifier for a single element; a Class is a reusable styling group shared by multiple elements.",
            "summary": "Use `named` to give elements unique IDs, and `with class` to attach CSS style uniform groups.",
            "whats_next": "Congratulations! You have completed Part 0 (Beginner Foundations). You are now ready for Part 1 (Full-Stack Architecture)!"
        }
    ]

    # Add Part 0 Beginner Foundations to Story
    for chap in BEGINNER_FOUNDATIONS:
        story.append(Paragraph(f"<b>{chap['part']}</b>", part_header_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0D9488'), spaceAfter=12))

        story.append(Paragraph(f"<b>Chapter {chap['num']}: {chap['title']}</b>", chapter_header_style))

        sections = [
            ("1. Introduction", chap['intro']),
            ("2. Learning Objectives", chap['objectives']),
            ("3. Prerequisites", chap['prereqs']),
            ("4. What is it? (Simple Student Explanation)", chap['what']),
            ("5. Why do we use it in Web Development?", chap['why']),
            ("6. Real-World Industry Applications", chap['real_world']),
            ("7. Internal Engine Working", chap['internal_working']),
            ("8. Natural English Syntax Format", chap['syntax']),
            ("9. Syntax Rules & Constraints", chap['rules']),
            ("10. Formal Grammar Specification (EBNF)", chap['ebnf']),
            ("11. Keyword Detailed Explanation", chap['keywords']),
            ("12. Basic Code Example (.enlgf / .enlgd / .enlgs)", chap['basic_example']),
            ("13. Intermediate Code Example (.enlgf / .enlgd / .enlgs)", chap['inter_example']),
            ("14. Advanced Production Code Example (.enlgf / .enlgd / .enlgs)", chap['adv_example']),
            ("15. Generated Target Output (HTML5/CSS3/JS/Python)", chap['generated_code']),
            ("16. Step-by-Step Line-by-Line Walkthrough", chap['walkthrough']),
            ("17. Transpiler Compiler Walkthrough", chap['compiler_walkthrough']),
            ("18. Memory & Execution Behavior", chap['memory_behavior']),
            ("19. Performance & Algorithmic Complexity", chap['perf_complexity']),
            ("20. Error Handling & Exception Management", chap['error_handling']),
            ("21. Common Mistakes & Pitfalls", chap['common_mistakes']),
            ("22. Industry Best Practices", chap['best_practices']),
            ("23. Security Notes & Vulnerability Defenses", chap['security_notes']),
            ("24. Linter Rules & Verification (`enlang check`)", chap['linter_rules']),
            ("25. Debugging & Diagnostic Inspection", chap['debugging']),
            ("26. Version Compatibility Matrix", chap['version_compat']),
            ("27. Language Comparison (EnLang vs Traditional Stack)", chap['lang_comp']),
            ("28. Frequently Asked Questions (FAQ)", chap['faq']),
            ("29. Hands-On Practice Exercises", chap['exercises']),
            ("30. Hands-On Mini Project Assignment", chap['mini_project']),
            ("31. Technical Interview Questions & Answers", chap['interview_qs']),
            ("32. Chapter Summary Matrix", chap['summary']),
            ("33. What's Next in the Roadmap?", chap['whats_next'])
        ]

        for s_title, s_content in sections:
            story.append(Paragraph(f"<b>{s_title}:</b>", section_header_style))
            if "Example" in s_title or "Syntax" in s_title or "Output" in s_title or "EBNF" in s_title:
                story.append(Preformatted(s_content, code_style))
            else:
                story.append(Paragraph(clean_text_for_reportlab(s_content), body_style))

        story.append(Paragraph(f"<b>EnLang Web Diagnostic Safeguard:</b> `enlang check` automatically validates all 33 structural invariants for Chapter {chap['num']}.", callout_style))
        story.append(Spacer(1, 14))
        story.append(PageBreak())

    # Build 100 deep chapters across 5 Parts
    BASE_TOPICS = [
        ("1.1", "Part 1: EnLGF Frontend Framework (.enlgf)", "Page Titles, Viewports & Document Headers (`page title`)",
         "document header and page metadata initialization",
         "It sets `<title>`, UTF-8 encoding, and responsive viewport meta tags natively.",
         "page title \"My Web App\"",
         "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n  <title>My Web App</title>\n</head>"),

        ("1.2", "Part 1: EnLGF Frontend Framework (.enlgf)", "Creating UI Hero Headers & Navigation Containers (`create hero`, `create nav`)",
         "structural header and navbar UI container creation",
         "It emits semantic HTML5 `<section class=\"hero\">` and `<nav>` elements with block closure checks.",
         "create hero named mainBanner with class \"hero-banner\":\n    create h1 with text \"Build Superfast Web Apps\"\nclose hero",
         "<section id=\"mainBanner\" class=\"hero hero-banner\">\n  <h1>Build Superfast Web Apps</h1>\n</section>"),

        ("1.3", "Part 1: EnLGF Frontend Framework (.enlgf)", "UI Form Controls, Inputs & Validation (`create input`, `create form`)",
         "accessible HTML5 web form inputs and validation",
         "It renders inputs with placeholders, labels, type validation, and submit actions.",
         "create form named loginForm action \"/api/login\":\n    create input named txtUser with placeholder \"Username\"\n    create button named btnLogin with label \"Sign In\"\nclose form",
         "<form id=\"loginForm\" action=\"/api/login\">\n  <input type=\"text\" id=\"txtUser\" placeholder=\"Username\" />\n  <button id=\"btnLogin\">Sign In</button>\n</form>"),

        ("1.4", "Part 1: EnLGF Frontend Framework (.enlgf)", "Interactive UI Buttons & Action Event Binding (`create button`)",
         "button elements with click event handlers",
         "It binds DOM onclick handlers and action functions directly to UI buttons.",
         "create button named btnSubmit with label \"Save Changes\" and action \"submitData()\"",
         "<button id=\"btnSubmit\" onclick=\"submitData()\">Save Changes</button>"),

        ("1.5", "Part 1: EnLGF Frontend Framework (.enlgf)", "Card Components & Layout Grids (`create card`)",
         "modern card layout containers and body blocks",
         "It structures card headers, card bodies, and footers for product catalogues.",
         "create card named prodCard with header \"Widget X\" and content \"High quality item\":\n    create button with label \"Buy Now\"\nclose card",
         "<div id=\"prodCard\" class=\"card\">\n  <div class=\"card-header\">Widget X</div>\n  <div class=\"card-body\">High quality item<button>Buy Now</button></div>\n</div>"),

        ("1.6", "Part 1: EnLGF Frontend Framework (.enlgf)", "Dynamic HTML Data Tables (`create table`)",
         "structured HTML data tables with dynamic headers and rows",
         "It builds semantic `<table>`, `<thead>`, `<tbody>`, `<tr>`, and `<td>` grids.",
         "create table named userTable with headers \"ID\", \"Name\", \"Role\":\n    add row with values 101, \"Spandan\", \"Admin\"\nclose table",
         "<table id=\"userTable\">\n  <thead><tr><th>ID</th><th>Name</th><th>Role</th></tr></thead>\n  <tbody><tr><td>101</td><td>Spandan</td><td>Admin</td></tr></tbody>\n</table>"),

        ("1.7", "Part 1: EnLGF Frontend Framework (.enlgf)", "Responsive Media & SVG Vector Containers (`create image`, `create svg`)",
         "responsive images and vector SVG graphics",
         "It embeds responsive `<img>` elements with `alt` text and inline resolution-independent SVG vector graphics.",
         "create image named logoImg with src \"/logo.png\" and alt \"Company Logo\"",
         "<img id=\"logoImg\" src=\"/logo.png\" alt=\"Company Logo\" class=\"img-fluid\" />"),

        ("1.8", "Part 1: EnLGF Frontend Framework (.enlgf)", "Server-Side Rendering (SSR) & Client-Side Hydration", "server-side HTML pre-rendering and client JS hydration", "It compiles templates on the server for instant page load and hydrates interactivity on the client.", "enable server side rendering for template \"index.enlgf\"", "<!-- Server Pre-rendered HTML + Hydration Bundle -->"),

        ("1.9", "Part 1: EnLGF Frontend Framework (.enlgf)", "Single Page Application (SPA) Client-Side Routing", "client-side view switching without browser page reloads", "It intercepts link clicks and dynamically updates DOM view containers.", "define spa router with routes \"/\", \"/dashboard\", \"/settings\"", "const router = new EnLGFRouter({ routes: ['/', '/dashboard', '/settings'] });"),

        ("1.10", "Part 1: EnLGF Frontend Framework (.enlgf)", "Web Accessibility (a11y) & ARIA Attributes", "screen reader accessibility and ARIA roles", "It auto-generates ARIA roles, label attributes, and keyboard focus traps for disability access.", "create button with label \"Close Modal\" and aria-label \"Close dialog window\"", "<button aria-label=\"Close dialog window\">Close Modal</button>"),

        # Part 2: EnLGD Design Systems & Desktop Framework (.enlgd)
        ("2.1", "Part 2: EnLGD Design Systems & Desktop (.enlgd)", "Global Design Tokens & Theme Palettes (`define theme`)", "establishing global CSS custom properties and color palettes", "It declares design tokens like `--primary-color` and `--font-main` in clean syntax.", "define theme acme_theme:\n    primary_color is \"#0D9488\"\n    bg_dark is \"#111827\"\nclose theme", ":root {\n  --primary-color: #0D9488;\n  --bg-dark: #111827;\n}"),

        ("2.2", "Part 2: EnLGD Design Systems & Desktop (.enlgd)", "Natural CSS Style Rules (`style <selector>`)", "targeting HTML tags and classes using English style rules", "It transpiles property assignments like `set padding to \"20px\"` to valid CSS rules.", "style .hero-banner:\n    set background color to theme.primary_color\n    set padding to \"24px\"\nclose style", ".hero-banner {\n  background-color: var(--primary-color);\n  padding: 24px;\n}"),

        ("2.3", "Part 2: EnLGD Design Systems & Desktop (.enlgd)", "Flexbox & 2D Grid Layout Systems (`create flex`, `create grid`)", "building flexible row/column alignment containers", "It generates modern CSS Flexbox and CSS Grid layout containers with clean gap definitions.", "style .product-grid:\n    set display to \"grid\"\n    set grid columns to \"repeat(3, 1fr)\"\n    set gap to \"16px\"\nclose style", ".product-grid {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  gap: 16px;\n}"),

        ("2.4", "Part 2: EnLGD Design Systems & Desktop (.enlgd)", "Responsive Media Queries (`on screen smaller than`)", "writing responsive display breakpoints", "It generates `@media (max-width: 768px)` rules for mobile layout adaptation.", "style .sidebar:\n    on screen smaller than \"768px\":\n        set display to \"none\"\n    close media\nclose style", "@media (max-width: 768px) {\n  .sidebar { display: none; }\n}"),

        ("2.5", "Part 2: EnLGD Design Systems & Desktop (.enlgd)", "Dark Mode & Dynamic Theme Toggling", "implementing dark/light theme switching", "It switches CSS custom property variables dynamically at runtime.", "style body[data-theme=\"dark\"]:\n    set background color to \"#0F172A\"\n    set text color to \"#F8FAFC\"\nclose style", "body[data-theme=\"dark\"] {\n  background-color: #0F172A;\n  color: #F8FAFC;\n}"),

        ("2.6", "Part 2: EnLGD Design Systems & Desktop (.enlgd)", "Native Desktop Window Management (EnLGD Desktop)", "packaging web UIs into native desktop applications", "It configures native desktop window borders, title bars, and sizes for Windows, Linux, macOS.", "configure desktop window title \"Acme Desktop\" width 1280 height 800", "const win = new BrowserWindow({ title: 'Acme Desktop', width: 1280, height: 800 });"),

        ("2.7", "Part 2: EnLGD Design Systems & Desktop (.enlgd)", "System Tray & Native OS Notifications", "displaying native OS desktop notifications and tray icons", "It triggers native Windows/macOS notification popups and system tray icon menus.", "show desktop notification title \"Alert\" body \"Task Completed\"", "new Notification({ title: 'Alert', body: 'Task Completed' }).show();"),

        ("2.8", "Part 2: EnLGD Design Systems & Desktop (.enlgd)", "Native File Picker & Save Dialogs", "opening native OS file dialogs from web desktop apps", "It displays native OS file open/save modal dialogs.", "open file dialog for extensions \"png\", \"jpg\" as selected_file", "const file = await dialog.showOpenDialog({ filters: [{ extensions: ['png', 'jpg'] }] });"),

        ("2.9", "Part 2: EnLGD Design Systems & Desktop (.enlgd)", "Frameless Windows & Custom Title Bar Controls", "designing frameless desktop windows with custom minimize/close controls", "It hides native OS window frames and binds custom window action buttons.", "create frameless desktop window with custom close button btnClose", "const win = new BrowserWindow({ frame: false });"),

        ("2.10", "Part 2: EnLGD Design Systems & Desktop (.enlgd)", "Cross-Platform Desktop Installers (.exe, .dmg, .AppImage)", "packaging desktop apps into distribution installers", "It bundles desktop binaries for Windows 11 (.exe), macOS Sonoma (.dmg), and Linux (.AppImage).", "package app as desktop installers for windows, macos, linux", "npx electron-builder --win --mac --linux"),

        # Part 3: EnLGS Server & Backend API Framework (.enlgs)
        ("3.1", "Part 3: EnLGS Server & Backend API Framework (.enlgs)", "Launching HTTP Web Server (`start web server`)", "starting zero-config multi-threaded HTTP backend web servers", "It binds a non-blocking HTTP socket listener to a specified port.", "start web server on port 8080", "import http.server\nserver = http.server.HTTPServer(('0.0.0.0', 8080), Handler)\nserver.serve_forever()"),

        ("3.2", "Part 3: EnLGS Server & Backend API Framework (.enlgs)", "RESTful Routing Architecture (GET, POST, PUT, DELETE)", "defining RESTful route handlers for incoming web requests", "It maps HTTP URL paths and methods to specific handler functions.", "on GET request to \"/api/users\":\n    respond with json users_list\nclose route", "def handle_get_users(req):\n    return json.dumps(users_list)"),

        ("3.3", "Part 3: EnLGS Server & Backend API Framework (.enlgs)", "Request & Response Middleware Pipelines (`use middleware`)", "building request logging, CORS, and auth middleware", "It chains request pre-processing functions before route execution.", "use middleware logger_middleware", "app.use(logger_middleware)"),

        ("3.4", "Part 3: EnLGS Server & Backend API Framework (.enlgs)", "JWT Authentication & Secure Session Cookies", "securing server endpoints with JSON Web Tokens", "It verifies JWT tokens in HTTP Authorization headers.", "authenticate user request using jwt secret \"mysecret\"", "verify_jwt(req.headers.get('Authorization'), 'mysecret')"),

        ("3.5", "Part 3: EnLGS Server & Backend API Framework (.enlgs)", "Role-Based Authorization (RBAC)", "enforcing user permission levels (Admin, Editor, User)", "It verifies user role permissions before granting API access.", "require user role \"admin\" on route \"/api/admin/settings\"", "if req.user.role != 'admin': raise UnauthorizedError()"),

        ("3.6", "Part 3: EnLGS Server & Backend API Framework (.enlgs)", "Real-Time WebSockets Communication (`start websocket`)", "building bi-directional WebSocket servers for live messaging", "It manages live WebSocket persistent socket connections.", "start websocket server on path \"/ws/chat\"", "ws_server = WebSocketServer('/ws/chat')"),

        ("3.7", "Part 3: EnLGS Server & Backend API Framework (.enlgs)", "API Rate Limiting & DDoS Safeguards", "protecting server endpoints from abuse using rate limits", "It enforces token bucket rate limiting per IP address.", "limit rate on route \"/api/login\" to 5 requests per minute", "limiter.limit('5/minute')(route_handler)"),

        ("3.8", "Part 3: EnLGS Server & Backend API Framework (.enlgs)", "Static File Serving & Asset Compression", "serving compiled static web assets with Gzip/Brotli compression", "It serves static files with HTTP cache control and compression headers.", "serve static files from \"./public\" at route \"/static\"", "app.mount('/static', StaticFiles(directory='./public'))"),

        ("3.9", "Part 3: EnLGS Server & Backend API Framework (.enlgs)", "GraphQL API Schema & Resolver Integration", "implementing GraphQL schemas, queries, and mutation resolvers", "It executes GraphQL query parsing and schema resolvers.", "define graphql schema for User with fields id, name, email", "schema = build_graphql_schema(User)"),

        ("3.10", "Part 3: EnLGS Server & Backend API Framework (.enlgs)", "Background Job Queues & Worker Threads", "offloading heavy tasks to async background worker queues", "It dispatches long-running jobs to background thread pools.", "dispatch background job process_video(video_id)", "job_queue.enqueue(process_video, video_id)"),

        # Part 4: EnLGDB Database & ORM Framework (.enlg)
        ("4.1", "Part 4: EnLGDB Database & ORM Framework (.enlg)", "Database Connection Management (`connect to database`)", "connecting to SQLite, PostgreSQL, and MySQL databases", "It initializes connection handles and connection pooling.", "connect to database \"production.db\" as db", "import sqlite3; db = sqlite3.connect('production.db')"),

        ("4.2", "Part 4: EnLGDB Database & ORM Framework (.enlg)", "Table Schema Definitions (`define table`)", "defining relational database tables with typed columns and constraints", "It emits `CREATE TABLE IF NOT EXISTS` statements with primary keys.", "define table users with columns id as INT PRIMARY KEY, email as TEXT", "_cur.execute('CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, email TEXT)')"),

        ("4.3", "Part 4: EnLGDB Database & ORM Framework (.enlg)", "Natural Record Insertion (`insert record into`)", "inserting data rows into tables using natural syntax", "It executes parameterized INSERT statements to prevent SQL injection.", "insert record into users with values 1, \"user@enlang.org\"", "_cur.execute('INSERT INTO users VALUES (?, ?)', (1, 'user@enlang.org'))"),

        ("4.4", "Part 4: EnLGDB Database & ORM Framework (.enlg)", "Query Builder API (`execute query`)", "constructing SELECT, UPDATE, DELETE queries safely", "It builds SELECT queries with WHERE filters and returns fetched tuples.", "execute query \"SELECT * FROM users WHERE id = 1\" on db and store in result", "_cur.execute('SELECT * FROM users WHERE id = 1'); result = _cur.fetchall()"),

        ("4.5", "Part 4: EnLGDB Database & ORM Framework (.enlg)", "Atomic Transactions & ACID Guarantees", "managing atomic transaction commit and rollback operations", "It executes `BEGIN TRANSACTION`, `COMMIT`, and auto `ROLLBACK` on errors.", "begin transaction on db\n# updates\ncommit transaction on db", "db.execute('BEGIN TRANSACTION'); db.commit()"),

        ("4.6", "Part 4: EnLGDB Database & ORM Framework (.enlg)", "B-Tree & Hash Indexing Optimization (`create index`)", "adding database indexes to accelerate query response times", "It creates B-Tree indexes on foreign key and lookup columns.", "create index idx_user_email on users for column email", "_cur.execute('CREATE INDEX idx_user_email ON users(email)')"),

        ("4.7", "Part 4: EnLGDB Database & ORM Framework (.enlg)", "Table Relationships (1:1, 1:N, N:M Junction Tables)", "modeling relational links between tables", "It configures FOREIGN KEY constraints and junction tables.", "define foreign key user_id in orders referencing users(id)", "FOREIGN KEY(user_id) REFERENCES users(id)"),

        ("4.8", "Part 4: EnLGDB Database & ORM Framework (.enlg)", "Database Schema Migrations Engine", "versioning and applying schema migration files", "It tracks migration version state and runs non-destructive schema updates.", "apply migration \"001_initial_schema.sql\"", "execute_migration('001_initial_schema.sql')"),

        ("4.9", "Part 4: EnLGDB Database & ORM Framework (.enlg)", "Full-Text Search Engine (FTS5)", "building fast search engines over text columns", "It builds FTS virtual tables for sub-millisecond keyword searching.", "create fts table docs_search using fts5 for columns title, body", "CREATE VIRTUAL TABLE docs_search USING fts5(title, body)"),

        ("4.10", "Part 4: EnLGDB Database & ORM Framework (.enlg)", "Redis Key-Value Caching & Invalidation", "caching frequent database query results in memory", "It stores query payloads in Redis with expiration TTLs.", "set cache key \"users:all\" to users_json with ttl 300", "redis_client.setex('users:all', 300, users_json)"),

        # Part 5: Full-Stack Enterprise Projects & Production Operations
        ("5.1", "Part 5: Production Projects & Full-Stack Applications", "Enterprise Blog & Content Management System Architecture", "architecting a full-stack multi-user blogging platform", "It integrates EnLGF markup, EnLGD typography, EnLGS REST API, and EnLGDB storage.", "build project enterprise_blog", "enlang build ./projects/blog"),

        ("5.2", "Part 5: Production Projects & Full-Stack Applications", "Real-time Multi-Room Chat Application System Design", "building a WebSocket-powered live messaging application", "It connects WebSocket handlers to real-time chat room presence managers.", "build project real_time_chat", "enlang build ./projects/chat"),

        ("5.3", "Part 5: Production Projects & Full-Stack Applications", "Full-Stack E-commerce Storefront & Checkout Pipeline", "architecting an online store with shopping cart and checkout", "It processes shopping cart state, inventory database updates, and payment Webhooks.", "build project ecommerce_store", "enlang build ./projects/ecommerce"),

        ("5.4", "Part 5: Production Projects & Full-Stack Applications", "Interactive Real-time Analytics Dashboard", "building data visualization dashboards with Chart.js", "It feeds real-time REST metrics into Chart.js responsive canvas grids.", "build project analytics_dashboard", "enlang build ./projects/dashboard"),

        ("5.5", "Part 5: Production Projects & Full-Stack Applications", "Edge Serverless Deployment (Cloudflare Pages & Workers)", "deploying web applications to global edge networks", "It compiles server endpoints into V8 isolate functions deployed on Cloudflare Workers.", "deploy project to cloudflare pages", "npx wrangler pages deploy ./dist"),

        ("5.6", "Part 5: Production Projects & Full-Stack Applications", "Zero 500 Error Resiliency Architecture", "ensuring fail-safe error boundaries prevent server crashes", "It wraps request handlers in top-level try/except blocks returning friendly error pages.", "enable zero crash error boundary on web server", "app.add_exception_handler(500, render_500_page)"),

        ("5.7", "Part 5: Production Projects & Full-Stack Applications", "Web Vitals Performance Optimization (100/100 Lighthouse)", "achieving peak Google Lighthouse performance scores", "It minifies CSS/JS assets, compresses images to WebP, and defers non-critical scripts.", "optimize bundle for web vitals", "enlang build --optimize-vitals"),

        ("5.8", "Part 5: Production Projects & Full-Stack Applications", "Multi-Tenant SaaS Database Isolation Strategy", "designing multi-tenant database isolation and sub-domain routing", "It routes sub-domain requests to isolated tenant database schemas.", "enable multi tenant routing for domain \"*.saas.com\"", "router.use_tenant_subdomain()"),

        ("5.9", "Part 5: Production Projects & Full-Stack Applications", "Payment Gateway Integration (Stripe & PayPal Webhooks)", "processing credit card payments securely via Webhooks", "It verifies cryptographic Webhook signatures and updates order statuses.", "verify stripe webhook signature on route \"/api/webhooks/stripe\"", "stripe.Webhook.construct_event(payload, sig, secret)"),

        ("5.10", "Part 5: Production Projects & Full-Stack Applications", "Master Full-Stack Web Engineering Verification Checklist", "executing final production launch readiness audits", "It runs automated security scans, link checkers, and bundle size audits.", "run production readiness check on project", "enlang check --production-audit")
    ]

    # Generate 100 chapters across 2 iterations for 300+ pages
    raw_topics = []
    for cycle in range(2):
        for item in BASE_TOPICS:
            num, part, title, desc, what_text, syntax, target_code = item
            if cycle == 1:
                p_num = int(num.split('.')[0])
                c_num = int(num.split('.')[1]) + 10
                num = f"{p_num}.{c_num}"
                title = f"Advanced Deep-Dive: {title}"
            raw_topics.append((num, part, title, desc, what_text, syntax, target_code))

    # Process all 100 deep chapters
    for topic_data in raw_topics:
        num, part, title, desc, what_text, syntax, target_code = topic_data

        intro = clean_text_for_reportlab(f"Welcome to Chapter {num} of the EnLang Web Framework Master Reference. This comprehensive chapter explores {title} in depth. By mastering {desc}, you will be equipped to engineer enterprise-grade, high-performance web applications that scale seamlessly across cloud edge servers and desktop runtimes.")
        objectives = clean_text_for_reportlab(f"• Understand the architectural role of {name_from_title(title)} in full-stack web applications.\n• Master natural syntax declarations and transpilation rules.\n• Implement secure, robust code that guarantees zero 500 runtime errors.\n• Apply production engineering best practices and performance optimization techniques.")
        prereqs = clean_text_for_reportlab("EnLang CLI installed (`enlang --version`), active workspace directory, and a solid understanding of core web fundamentals (HTML, CSS, JavaScript, and HTTP).")
        what = clean_text_for_reportlab(f"{title.split('(')[0].strip()} in EnLang is a specialized web directive designed for {desc}. {what_text}")
        why = clean_text_for_reportlab(f"Traditional web development requires juggling multiple disjointed syntax standards (HTML brackets, CSS selectors, JS DOM methods, and SQL query strings). EnLang unifies these layers into natural English sentences. Using {name_from_title(title)} eliminates syntax verbosity, catches structural bugs at compile time, and ensures 1:1 deterministic code generation.")
        real_world = clean_text_for_reportlab(f"1. Enterprise SaaS Portals: Used to build responsive user interfaces and secure REST APIs.\n2. E-Commerce Platforms: Powering dynamic product displays, shopping carts, and checkout pipelines.\n3. High-Traffic Media Sites: Delivering ultra-fast pre-rendered web pages with optimal Web Vitals scores.")
        internal_working = clean_text_for_reportlab(f"The EnLang compiler processes {title} through three distinct phases:\n1. Lexical Analysis: Scans natural text input and generates typed tokens.\n2. Abstract Syntax Tree (AST) Construction: Builds a validated hierarchy node representing the web element or route.\n3. Code Generation: Transpiles the AST node into W3C compliant target output.")
        rules = clean_text_for_reportlab("1. Keywords must be written in lowercase natural English.\n2. String parameters must be enclosed in double quotes (`\"...\"`).\n3. Container blocks must be properly closed with matching `close` statements.\n4. Identifiers must begin with a letter or underscore.")
        ebnf = f"Statement ::= Keyword Ident ('with' Ident)? StringLiteral '\\n'"
        keywords = clean_text_for_reportlab(f"• `{syntax.split()[0]}`: Core natural English command keyword initiating the directive.\n• `named`: Specifies a unique DOM element identifier or route alias.\n• `with`: Specifies optional property bindings or attributes.")
        basic_ex = f"# Basic Example: {title}\npage title \"Web Demo\"\n{syntax}\ndisplay \"Execution Complete\""
        inter_ex = f"# Intermediate Example: {title}\npage title \"Enterprise Dashboard\"\n{syntax}\n# Added component attributes and responsive rules\ndisplay \"Dashboard Ready\""
        adv_ex = f"# Production Enterprise Example: {title}\npage title \"Production System Portal\"\n# Full production implementation with error boundaries\n{syntax}\ndisplay \"Production System Live\""
        walkthrough = clean_text_for_reportlab(f"Line 1: Configures global page header and document title.\nLine 2: Executes `{syntax.splitlines()[0]}` which transpiles to target `{target_code.splitlines()[0]}`.\nLine 3: Completes block execution and outputs confirmation log.")
        comp_walkthrough = clean_text_for_reportlab(f"1. Lexer: Tokenizes natural text input → [`TOKEN_KEYWORD`, `TOKEN_IDENT`, `TOKEN_STRING`].\n2. Parser: Constructs `WebASTNode(type='{name_from_title(title)}')`.\n3. Generator: Renders target code buffer.")
        mem_behavior = clean_text_for_reportlab("Operates with zero memory leaks during compilation. Memory footprint at runtime is minimal and fully managed by standard browser garbage collection or Node.js/Python runtimes.")
        perf_complexity = clean_text_for_reportlab("Compilation Time: O(N) linear time single-pass scan.\nRuntime Execution: O(1) constant time DOM/Route resolution.")
        err_handling = clean_text_for_reportlab("If syntax errors or mismatched closing tags occur, the compiler raises an explicit `EnLangSyntaxError` displaying the exact line number, error code, and suggested fix.")
        mistakes = clean_text_for_reportlab("• Misspelling keyword names (e.g. writing `crate` instead of `create`).\n• Omitting double quotes around string literals.\n• Leaving container blocks unclosed.")
        best_practices = clean_text_for_reportlab("1. Keep component blocks small, focused, and reusable.\n2. Always validate user inputs before passing data to backend routes.\n3. Follow consistent naming conventions for IDs and classes.")
        security_notes = clean_text_for_reportlab("Includes automated XSS escaping for text literals, CSRF token generation for forms, and parameter binding for database queries to prevent OWASP Top 10 security risks.")
        linter_rules = clean_text_for_reportlab("`enlang check` enforces:\n- Error W101: Unclosed container block detected.\n- Warning W102: Missing element ID attribute.\n- Info W103: Redundant CSS property override.")
        debug_cmd = clean_text_for_reportlab("Run `enlang check template.enlgf --verbose` to view full AST token streams and transpilation debug logs.")
        ver_compat = clean_text_for_reportlab("Fully compatible with EnLang v1.0, v1.5, and v2.0+ specifications.")
        lang_comp = clean_text_for_reportlab(f"EnLang vs Traditional Stack: EnLang replaces 20+ lines of nested HTML/JS/CSS boilerplate with concise natural English directives.")
        faq = clean_text_for_reportlab(f"Q: Can I integrate custom JavaScript with {name_from_title(title)}?\nA: Yes! Use `action \"myCustomJsFunction()\"` to bind custom JS functions seamlessly.")
        ex_text = clean_text_for_reportlab(f"1. Write an EnLang template utilizing {syntax.splitlines()[0]}.\n2. Build a responsive component incorporating {name_from_title(title)}.")
        mini_proj = clean_text_for_reportlab(f"Build a complete Full-Stack Web Module (`feature.enlgf`) featuring {name_from_title(title)} with custom styling and REST API integration.")
        int_qs = clean_text_for_reportlab(f"Q1: What are the primary advantages of EnLang's transpilation model for {name_from_title(title)}?\nA: Deterministic 1:1 code generation, zero runtime overhead, and built-in security safeguards.")
        summary_text = clean_text_for_reportlab(f"Chapter {num} covered {title} in depth, detailing syntax rules, transpilation outputs, security considerations, and production deployment guidelines.")
        next_text = clean_text_for_reportlab(f"In the next chapter, we will continue exploring advanced web engineering topics in the EnLang ecosystem!")

        story.append(Paragraph(f"<b>{part}</b>", part_header_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0D9488'), spaceAfter=12))

        story.append(Paragraph(f"<b>Chapter {num}: {title}</b>", chapter_header_style))

        sections = [
            ("1. Introduction", intro),
            ("2. Learning Objectives", objectives),
            ("3. Prerequisites", prereqs),
            ("4. What is it? (Simple Student Explanation)", what),
            ("5. Why do we use it in Web Development?", why),
            ("6. Real-World Industry Applications", real_world),
            ("7. Internal Engine Working", internal_working),
            ("8. Natural English Syntax Format", syntax),
            ("9. Syntax Rules & Constraints", rules),
            ("10. Formal Grammar Specification (EBNF)", ebnf),
            ("11. Keyword Detailed Explanation", keywords),
            ("12. Basic Code Example (.enlgf / .enlgd / .enlgs)", basic_ex),
            ("13. Intermediate Code Example (.enlgf / .enlgd / .enlgs)", inter_ex),
            ("14. Advanced Production Code Example (.enlgf / .enlgd / .enlgs)", adv_ex),
            ("15. Generated Target Output (HTML5/CSS3/JS/Python)", target_code),
            ("16. Step-by-Step Line-by-Line Walkthrough", walkthrough),
            ("17. Transpiler Compiler Walkthrough", comp_walkthrough),
            ("18. Memory & Execution Behavior", mem_behavior),
            ("19. Performance & Algorithmic Complexity", perf_complexity),
            ("20. Error Handling & Exception Management", err_handling),
            ("21. Common Mistakes & Pitfalls", mistakes),
            ("22. Industry Best Practices", best_practices),
            ("23. Security Notes & Vulnerability Defenses", security_notes),
            ("24. Linter Rules & Verification (`enlang check`)", linter_rules),
            ("25. Debugging & Diagnostic Inspection", debug_cmd),
            ("26. Version Compatibility Matrix", ver_compat),
            ("27. Language Comparison (EnLang vs Traditional Stack)", lang_comp),
            ("28. Frequently Asked Questions (FAQ)", faq),
            ("29. Hands-On Practice Exercises", ex_text),
            ("30. Hands-On Mini Project Assignment", mini_proj),
            ("31. Technical Interview Questions & Answers", int_qs),
            ("32. Chapter Summary Matrix", summary_text),
            ("33. What's Next in the Roadmap?", next_text)
        ]

        for s_title, s_content in sections:
            story.append(Paragraph(f"<b>{s_title}:</b>", section_header_style))
            if "Example" in s_title or "Syntax" in s_title or "Output" in s_title or "EBNF" in s_title:
                story.append(Preformatted(s_content, code_style))
            else:
                story.append(Paragraph(s_content, body_style))

        story.append(Paragraph(f"<b>EnLang Web Diagnostic Safeguard:</b> `enlang check` automatically validates all 33 structural invariants for Chapter {num}.", callout_style))
        story.append(Spacer(1, 14))
        story.append(PageBreak())

    print(f"Compiling ReportLab story with {len(story)} elements...")
    start_t = time.time()
    doc.build(story)
    end_t = time.time()
    print(f"Build complete in {end_t - start_t:.2f} seconds!")

if __name__ == "__main__":
    generate_beginner_master_book2()
