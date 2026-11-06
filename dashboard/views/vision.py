import json
import re

import streamlit as st

import common
import launcher

st.title("📷 Visão computacional")
st.caption(
    "Modelos da Fase 6 executados localmente: YOLOv5 adaptado (controle PS5 e garrafa térmica), "
    "YOLOv5 padrão (COCO) e CNN construída do zero."
)

SAMPLES_DIR = common.FASE6_DIR / "samples"
OUTPUTS_DIR = common.FASE6_DIR / "outputs"
UPLOADS_DIR = OUTPUTS_DIR / "uploads"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

MODELS = {
    "yolo-60": "YOLOv5 adaptado (60 épocas)",
    "yolo-30": "YOLOv5 adaptado (30 épocas)",
    "yolo-coco": "YOLOv5 padrão (COCO)",
    "cnn": "CNN construída do zero",
}

# ============================
# PARÂMETROS
# ============================

col_model, col_source = st.columns(2)

with col_model:
    model_key = st.radio(
        "Modelo",
        list(MODELS),
        format_func=MODELS.get,
    )

    confidence = 0.25

    if model_key != "cnn":
        confidence = st.slider("Confiança mínima", 0.05, 0.95, 0.25, 0.05)

with col_source:
    source_type = st.radio(
        "Imagens",
        ["Todas as imagens de teste", "Uma imagem de teste", "Enviar uma imagem"],
    )

    source_path = SAMPLES_DIR

    if source_type == "Uma imagem de teste":
        samples = sorted(
            path.name for path in SAMPLES_DIR.iterdir()
            if path.suffix.lower() in IMAGE_EXTENSIONS
        )
        source_path = SAMPLES_DIR / st.selectbox("Imagem", samples)

    elif source_type == "Enviar uma imagem":
        uploaded = st.file_uploader("Imagem (JPG ou PNG)", type=["jpg", "jpeg", "png"])

        if uploaded:
            UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
            safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", uploaded.name)
            source_path = UPLOADS_DIR / safe_name
            source_path.write_bytes(uploaded.getvalue())
        else:
            source_path = None

# ============================
# EXECUÇÃO
# ============================

if st.button("Executar modelo", type="primary", disabled=source_path is None):
    extra_args = ["--source", str(source_path)]

    if model_key != "cnn":
        extra_args += ["--conf", str(confidence)]

    with st.spinner(f"Executando {MODELS[model_key]}... (a primeira execução pode demorar)"):
        try:
            result = launcher.run_service(
                f"fase6-{model_key}",
                capture_output=True,
                extra_args=extra_args,
            )
            st.session_state.vision_result = {
                "model": model_key,
                "success": result.returncode == 0,
                "output": (result.stdout or "") + (result.stderr or ""),
            }
        except RuntimeError as error:
            st.session_state.vision_result = {
                "model": model_key,
                "success": False,
                "output": str(error),
            }

# ============================
# RESULTADOS
# ============================


def find_annotated_image(output_dir, image_name):
    # O YOLOv5 salva as imagens anotadas com extensão .jpg.
    stem = image_name.rsplit(".", 1)[0]

    for candidate in sorted(output_dir.glob(f"{stem}.*")):
        if candidate.suffix.lower() in IMAGE_EXTENSIONS:
            return candidate

    return None


def build_rows(model, results):
    rows = []

    for item in results:
        if model == "cnn":
            status = "-"

            if item.get("correct") is not None:
                status = "Correto" if item["correct"] else f"Incorreto (esperado: {item['expected_class']})"

            rows.append({
                "Imagem": item["image"],
                "Classe prevista": item["predicted_class"],
                "Confiança": item["confidence"],
                "Resultado": status,
            })
            continue

        if not item["detections"]:
            rows.append({"Imagem": item["image"], "Classe": "nenhuma detecção", "Confiança": None})

        for detection in item["detections"]:
            rows.append({
                "Imagem": item["image"],
                "Classe": detection["class"],
                "Confiança": detection["confidence"],
            })

    return rows


result = st.session_state.get("vision_result")

if result:
    if not result["success"]:
        st.error("Não foi possível executar o modelo.")
        st.code(result["output"].strip(), language="text")
        st.stop()

    output_dir = OUTPUTS_DIR / result["model"]
    summary = json.loads((output_dir / "detections.json").read_text(encoding="utf-8"))

    st.success(f"{summary['model_label']} · executado em {summary['generated_at']}")

    st.dataframe(
        build_rows(result["model"], summary["results"]),
        width="stretch",
        hide_index=True,
    )

    columns = st.columns(3)

    for index, item in enumerate(summary["results"]):
        image_path = find_annotated_image(output_dir, item["image"])

        if image_path:
            columns[index % 3].image(str(image_path), caption=item["image"], width="stretch")

    with st.expander("Saída completa do serviço"):
        st.code(result["output"].strip(), language="text")
