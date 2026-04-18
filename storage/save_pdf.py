import os
from fpdf import FPDF


class _PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
        self.set_text_color(0)


def _safe(text):
    """Strip characters outside latin-1 range so built-in fonts don't crash."""
    return text.encode("latin-1", errors="replace").decode("latin-1")


def save_pdf(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    pdf = _PDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    is_qa = data and "question" in data[0]

    # Title
    pdf.set_font("Helvetica", "B", 18)
    title = "Interview Questions" if is_qa else "Scraped Data"
    pdf.cell(0, 12, title, ln=True, align="C")
    pdf.set_draw_color(100, 100, 220)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    for i, item in enumerate(data, 1):
        if is_qa:
            # Question
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_fill_color(240, 240, 255)
            q_text = _safe(f"Q{i}.  {item.get('question', '')}")
            pdf.multi_cell(0, 8, q_text, fill=True)
            pdf.ln(1)

            # Answer
            answer = item.get("answer", "")
            if answer:
                pdf.set_font("Helvetica", "", 10)
                pdf.set_x(14)
                pdf.multi_cell(186, 6, _safe(answer))
            pdf.ln(5)
        else:
            # Generic key-value record — key and value on separate lines
            pdf.set_font("Helvetica", "B", 10)
            pdf.multi_cell(0, 7, f"Record {i}")
            for key, value in item.items():
                pdf.set_font("Helvetica", "B", 9)
                pdf.multi_cell(0, 6, _safe(str(key)) + ":")
                pdf.set_font("Helvetica", "", 9)
                # Truncate extremely long unbreakable strings to avoid layout crash
                val_str = _safe(str(value))[:2000]
                pdf.multi_cell(0, 6, val_str)
                pdf.ln(1)
            pdf.ln(3)

    pdf.output(path)
    print(f"Saved PDF to {path}")
