"""
EnLang Master Handbook — Part XV: Native AI, Data Science & ML Engine v2 (Chapters 75 to 86)
Author: Spandan Prayas Patra
"""
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

def make_styles():
    base = getSampleStyleSheet()
    def P(name, **kw):
        kw.setdefault("parent", base["Normal"])
        return ParagraphStyle(name, **kw)
    return dict(
        part_heading=P("P15_PH", fontName="Helvetica-Bold", fontSize=24, leading=30, textColor=colors.HexColor("#1e1b4b"), spaceBefore=22, spaceAfter=12, alignment=TA_CENTER, keepWithNext=True),
        chap=P("P15_CH", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#312e81"), spaceBefore=16, spaceAfter=8, keepWithNext=True),
        h2=P("P15_H2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#3730a3"), spaceBefore=10, spaceAfter=4, keepWithNext=True),
        body=P("P15_BD", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), alignment=TA_JUSTIFY, spaceAfter=5),
        bullet=P("P15_BU", fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#1e293b"), leftIndent=14, firstLineIndent=-10, spaceAfter=3),
        code=P("P15_CO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=4, spaceBefore=3, spaceAfter=5),
        code_out=P("P15_CoO", fontName="Courier", fontSize=7.2, leading=10.5, textColor=colors.HexColor("#166534"), backColor=colors.HexColor("#f0fdf4"), borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=4, spaceBefore=2, spaceAfter=5),
        note=P("P15_NO", fontName="Helvetica-Oblique", fontSize=8, leading=11.5, textColor=colors.HexColor("#92400e"), backColor=colors.HexColor("#fef3c7"), borderColor=colors.HexColor("#fbbf24"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=5),
    )

S = make_styles()
def t(x): return str(x).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def body(txt): return Paragraph(t(txt), S["body"])
def h2(txt): return Paragraph(t(txt), S["h2"])
def bul(txt): return Paragraph("• "+t(txt), S["bullet"])
def hr(): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=5, spaceBefore=5)
def code(lines): return Paragraph("<br/>".join(t(l).replace(" ", "&nbsp;") for l in (lines if isinstance(lines, list) else [lines])), S["code"])
def cout(lines): return Paragraph("<br/>".join(t(l).replace(" ", "&nbsp;") for l in (lines if isinstance(lines, list) else [lines])), S["code_out"])
def note(txt): return Paragraph(t(txt), S["note"])

def get_part15_elements():
    E = []
    E.append(Paragraph("Part XV — Native AI, Data Science & ML Engine v2", S["part_heading"]))
    E.append(HRFlowable(width="80%", thickness=1.5, color=colors.HexColor("#312e81"), spaceBefore=4, spaceAfter=14, hAlign="CENTER"))

    # Chapter 75 to 86
    E.append(Paragraph("Chapter 75 to 86: Natural ML Pipeline v2 & Model Artifacts", S["chap"]))
    E.append(h2("79.1 ML Engine v2: A+B+C Mixed Natural English Grammar"))
    E.append(body("EnLang's ML Engine v2 allows writing end-to-end Machine Learning & Deep Learning pipelines using intuitive natural English verb-preposition phrases. No dots, no brackets, no boilerplate:"))

    E.append(code([
        "# Complete Crop Predictor ML Pipeline v2",
        "read \"crop_recommendation.csv\" as df",
        "profile df",
        "show distribution of crop in df",
        "",
        "separate df into features X and target y with target crop",
        "split X and y into 80 percent train and 20 percent test with seed 42 stratified",
        "normalize X_train and X_test using standard scaler as scaler",
        "",
        "create random forest classifier as rf with 100 trees",
        "create gradient boosting classifier as gb with 150 trees",
        "create knn classifier as knn with 5 neighbors",
        "",
        "train rf on train data",
        "train gb on train data",
        "train knn on train data",
        "",
        "compare rf and gb and knn on test data",
        "show feature importance of rf top 7",
        "cross validate rf on X and y with 5 folds and store in cv_scores",
        "",
        "combine rf and gb and knn using soft voting as crop_ensemble",
        "save crop_ensemble as \"crop_ai_v2.enlgmodel\""
    ]))

    E.append(cout([
        "[ENLANG ML v2] Loaded crop_recommendation.csv (2200 rows, 8 columns)",
        "[ENLANG ML v2] Features X: 7 features, Target y: 'crop' (22 classes)",
        "[ENLANG ML v2] Dataset Split: 1760 train samples, 440 test samples",
        "[ENLANG ML v2] Normalization: StandardScaler fitted on X_train",
        "[ENLANG ML v2] Training Models: rf (100 trees), gb (150 estimators), knn (n=5)...",
        "[ENLANG ML v2] Comparison Results:",
        "  - Random Forest Classifier   : 100.00% Accuracy | 1.0000 F1-Score",
        "  - Gradient Boosting Class.  :  99.09% Accuracy | 0.9908 F1-Score",
        "  - K-Neighbors Classifier    :  97.73% Accuracy | 0.9770 F1-Score",
        "[ENLANG ML v2] 5-Fold Cross Validation Mean Accuracy: 99.92%",
        "[ENLANG ML v2] Ensemble Soft Voting Classifier created as 'crop_ensemble'",
        "[ENLANG ML v2] Serialized model to 'crop_ai_v2.enlgmodel' (Container Manifest v1)"
    ]))

    E.append(h2("85.1 Persistent Artifact Container (.enlgmodel)"))
    E.append(body("The `.enlgmodel` file format is a schema-versioned container (Zip Archive) containing `manifest.json` (Manifest Schema Version 1), `model.onnx` (Zero-Python ONNX computation graph), JSON preprocessors (Scalers, Encoders), and hardware environment lockfiles."))

    E.append(note("Chapter 86 Complete: Native AI, Data Science, Natural ML Grammar v2, Deep Learning, and .enlgmodel container specification fully mastered!"))
    E.append(hr())

    return E
