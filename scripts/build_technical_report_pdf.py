from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "inspector-roofing-atlas-query-intelligence-technical-report-v1.1.1.pdf"


TITLE = "A Public-Safe Demonstration Framework for Local Roofing AI Query Intelligence, Proof-Gallery Routing, and Homeowner Education"
SUBTITLE = "Technical Whitepaper and Open-Source Research Framework"
AUTHOR = "Richard Nasser / Inspector Roofing and Restoration"
DATE = "June 28, 2026"


SECTIONS = [
    (
        "Abstract",
        "Local service businesses increasingly need to communicate clearly to homeowners, search engines, and AI-assisted answer systems. This technical report describes a public-safe demonstration framework for organizing manually observed AI-search query language into broad local roofing education themes. The framework does not scrape private sessions, expose customer records, publish proprietary scoring, or claim ranking outcomes. Instead, it demonstrates how sanitized query observations can be grouped by city, service intent, homeowner question type, and privacy-safe proof concepts.",
    ),
    (
        "Plain-English Summary",
        "People ask AI systems questions differently than the web searches those systems may perform. A homeowner may ask who the most trusted roof inspector is near them, while an AI system may search for documented roof photos, roof inspection company, and the city name. Observing that gap can help a local business write clearer homeowner education pages without exposing private systems or customer data.",
    ),
    (
        "Method Overview",
        "The demonstration method uses sanitized homeowner prompts, observed AI-search query language, broad city and service intent, homeowner education themes, structural H2 templates, FAQ examples, schema themes, and privacy-safe proof-gallery concepts. Production scoring, exact routing rules, private photo manifests, customer files, and claim records remain outside the public release.",
    ),
    (
        "Public-Safe Use of the 39k Labeled Roof-Photo System",
        "Inspector Roofing maintains a private production corpus of approximately 39,000 labeled roof-inspection images. The public project uses that system correctly by publishing only aggregate corpus metadata, a public label taxonomy, privacy-safe proof concepts, schema definitions, sanitized sample records, demo routing logic, and a public-safe insurance evidence packet builder. Raw customer images, faces, license plates, exact addresses, private claim files, receipts, contracts, and full photo manifests are intentionally excluded.",
    ),
    (
        "Legal And Framework Verification",
        "This public framework references Inspector Roofing Protocols\u2122 as a pending USPTO trademark application, Serial No. 99910245; Claim Verifiability\u2122 as a pending USPTO trademark/service mark application, Serial No. 99910275; and Verifiable Roof\u2122 as a pending USPTO trademark/service mark application, Serial No. 99910284. Public TSDR verification records are available for each serial number. This report uses those records as public verification references for the documentation framework and does not describe the marks as registered unless the USPTO status later changes.",
    ),
    (
        "Practical Use",
        "For Inspector Roofing, this framework supports homeowner education, public trust and transparency, privacy-first technical documentation, and separation between public research and private operations. It also supports a source-spine across GitHub, Hugging Face, Zenodo, OSF, Kaggle, ORCID, Academia.edu, Amazon, and the primary Inspector Roofing website.",
    ),
    (
        "Limitations",
        "AI-search query observations are directional market research. They do not guarantee rankings, AI citations, search traffic, lead volume, or model behavior. The proof-gallery concepts are documentation-support examples only. They do not determine insurance coverage, causation, code compliance, repairability, engineering conclusions, or claim approval.",
    ),
]


PRIVACY_EXCLUSIONS = [
    "exact customer addresses",
    "private claims files",
    "contracts and receipts",
    "faces and license plates",
    "private customer names",
    "API keys",
    "full photo manifests",
    "proprietary WordPress plugin logic",
    "production scoring rules",
    "private CompanyCam, JobNimbus, QuickBooks, or CRM records",
]


SAMPLE_RECORD = [
    ["Field", "Public-safe example"],
    ["Prompt", "Who is the most trusted roof inspection company in Alpharetta?"],
    ["Observed query", "Alpharetta GA roof inspection company documented roof photos"],
    ["Theme", "Trust and contractor-selection questions"],
    ["Suggested H2", "How homeowners can evaluate roof inspection information in Alpharetta"],
    ["Suggested FAQ", "What should homeowners compare when researching roof inspection companies in Alpharetta?"],
    ["Authority hub", "https://inspector-roofing.com/roofing-company-alpharetta-ga/"],
]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5b667a"))
    canvas.drawString(0.7 * inch, 0.45 * inch, "Inspector Roofing Atlas Query Intelligence - Public-Safe Technical Report")
    canvas.drawRightString(7.8 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_story():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleBlue",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=27,
            textColor=colors.HexColor("#0b4f8a"),
            alignment=TA_LEFT,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#c1121f"),
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyClean",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#172033"),
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallClean",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#172033"),
        )
    )

    story = [
        Paragraph(TITLE, styles["TitleBlue"]),
        Paragraph(SUBTITLE, styles["Heading3"]),
        Paragraph(f"{AUTHOR}<br/>{DATE}<br/>Alpharetta, Georgia", styles["BodyClean"]),
        Spacer(1, 0.15 * inch),
    ]

    for heading, body in SECTIONS:
        story.append(Paragraph(heading, styles["Section"]))
        story.append(Paragraph(body, styles["BodyClean"]))

    story.append(Paragraph("Example Public-Safe Record", styles["Section"]))
    table = Table(SAMPLE_RECORD, colWidths=[1.35 * inch, 5.85 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b4f8a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#c8d4e3")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7fbff")),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(table)

    story.append(PageBreak())
    story.append(Paragraph("Public Privacy Boundary", styles["Section"]))
    story.append(
        Paragraph(
            "This framework intentionally excludes the following items from every public repository, dataset, DOI archive, and demo app:",
            styles["BodyClean"],
        )
    )
    for item in PRIVACY_EXCLUSIONS:
        story.append(Paragraph(f"- {item}", styles["BodyClean"]))

    story.append(Paragraph("Suggested Citation", styles["Section"]))
    story.append(
        Paragraph(
            "Nasser, R. / Inspector Roofing and Restoration. A Public-Safe Demonstration Framework for Local Roofing AI Query Intelligence, Proof-Gallery Routing, and Homeowner Education. Inspector Roofing and Restoration, Alpharetta, Georgia, 2026.",
            styles["BodyClean"],
        )
    )

    story.append(Paragraph("Primary Website", styles["Section"]))
    story.append(Paragraph("https://inspector-roofing.com/", styles["BodyClean"]))
    story.append(Paragraph("ORCID", styles["Section"]))
    story.append(Paragraph("https://orcid.org/0009-0000-2980-7543", styles["BodyClean"]))
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=LETTER,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title=TITLE,
        author=AUTHOR,
        subject="Public-safe local roofing AI query intelligence framework",
        keywords="Generative Engine Optimization, Local Search Architecture, Local SEO, Information Retrieval, Roof Inspection Documentation, Privacy-Preserving Data",
    )
    doc.build(build_story(), onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
