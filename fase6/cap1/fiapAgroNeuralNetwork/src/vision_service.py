"""
Serviço de visão computacional da Fase 6 (Agro Neural Network).

Executa localmente os modelos treinados no Google Colab:
- YOLOv5 adaptado (30 e 60 épocas): detecção de controle PS5 e garrafa térmica
- YOLOv5 padrão (pesos COCO): detecção de objetos genéricos
- CNN construída do zero: classificação entre controle PS5 e garrafa térmica

Uso:
    python src/vision_service.py --model yolo-60
    python src/vision_service.py --model cnn --source samples/garrafa_014.jpeg

As imagens anotadas e o resumo (detections.json) são salvos em outputs/<modelo>.
"""

import argparse
import contextlib
import importlib
import json
import os
import pathlib
import sys
import types
from datetime import datetime
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_DIR / "models"
SAMPLES_DIR = PROJECT_DIR / "samples"
OUTPUTS_DIR = PROJECT_DIR / "outputs"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

YOLO_REPOSITORY = "ultralytics/yolov5"

MODELS = {
    "yolo-60": {
        "label": "YOLOv5 adaptado (60 épocas)",
        "type": "yolo",
        "weights": MODELS_DIR / "yolo" / "60_epochs" / "best.pt",
    },
    "yolo-30": {
        "label": "YOLOv5 adaptado (30 épocas)",
        "type": "yolo",
        "weights": MODELS_DIR / "yolo" / "30_epochs" / "best.pt",
    },
    "yolo-coco": {
        "label": "YOLOv5 padrão (pesos COCO)",
        "type": "yolo",
        "weights": None,
    },
    "cnn": {
        "label": "CNN construída do zero (30 épocas)",
        "type": "cnn",
        "weights": MODELS_DIR / "cnn" / "cnn_30_epocas.keras",
    },
}

# Mesmas classes e pré-processamento utilizados no treinamento da CNN.
CNN_CLASSES = {
    0: "controle_ps5",
    1: "garrafa_termica",
}
CNN_IMAGE_SIZE = (128, 128)

# Mesma regra do notebook: o prefixo do arquivo indica a classe real.
FILE_PREFIX_CLASSES = {
    "controle": "controle_ps5",
    "garrafa": "garrafa_termica",
}

BANNER_COLORS = {
    True: (31, 125, 74),     # acerto
    False: (192, 57, 43),    # erro
    None: (52, 73, 94),      # classe real desconhecida
}


# ============================
# ENTRADAS
# ============================

def collect_images(source):
    source = Path(source).expanduser().resolve()

    if source.is_file():
        return [source]

    if source.is_dir():
        return sorted(
            path for path in source.iterdir()
            if path.suffix.lower() in IMAGE_EXTENSIONS
        )

    raise FileNotFoundError(f"Imagem ou pasta não encontrada: {source}")


# ============================
# YOLOv5
# ============================

@contextlib.contextmanager
def checkpoint_path_compatibility():
    """
    Permite abrir os pesos treinados no Google Colab em outras versões do Python.

    O checkpoint do YOLOv5 guarda caminhos (objetos Path) das configurações
    do treino. No Colab (Python 3.13+), esses objetos ficam registrados no
    módulo interno pathlib._local, que não existe no Python 3.12 ou anterior.
    Além disso, caminhos do Linux (PosixPath) não podem ser criados no Windows.
    As adaptações são temporárias e desfeitas após o carregamento.
    """
    added_shim = False

    try:
        importlib.import_module("pathlib._local")  # Python 3.13+
    except ModuleNotFoundError:
        shim = types.ModuleType("pathlib._local")

        for name in (
            "Path",
            "PurePath",
            "PosixPath",
            "WindowsPath",
            "PurePosixPath",
            "PureWindowsPath",
        ):
            setattr(shim, name, getattr(pathlib, name))

        sys.modules["pathlib._local"] = shim
        added_shim = True

    path_modules = [pathlib, sys.modules["pathlib._local"]]
    original_posix_paths = [module.PosixPath for module in path_modules]

    if os.name == "nt":
        for module in path_modules:
            module.PosixPath = pathlib.WindowsPath

    try:
        yield

    finally:
        for module, original in zip(path_modules, original_posix_paths):
            module.PosixPath = original

        if added_shim:
            sys.modules.pop("pathlib._local", None)


def load_yolo_model(config, confidence):
    # Os pesos foram gerados pelo próprio projeto e são confiáveis.
    # A partir do PyTorch 2.6, o carregamento padrão (weights_only=True)
    # bloqueia checkpoints completos do YOLOv5, por isso é desativado aqui.
    os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")

    import torch

    print("Carregando o YOLOv5 via torch.hub...")
    print("(na primeira execução, o código do YOLOv5 é baixado do GitHub)")

    if config["weights"] is None:
        model = torch.hub.load(YOLO_REPOSITORY, "yolov5s", trust_repo=True)
    else:
        if not config["weights"].exists():
            raise FileNotFoundError(f"Pesos não encontrados: {config['weights']}")

        with checkpoint_path_compatibility():
            model = torch.hub.load(
                YOLO_REPOSITORY,
                "custom",
                path=str(config["weights"]),
                trust_repo=True,
            )

    model.conf = confidence

    return model


def run_yolo(config, images, output_dir, confidence):
    model = load_yolo_model(config, confidence)

    results = model([str(image) for image in images], size=640)

    # Salva as imagens com as caixas delimitadoras, classes e confiança.
    results.save(save_dir=str(output_dir), exist_ok=True)

    summary = []

    for image, detections in zip(images, results.pandas().xyxy):
        summary.append({
            "image": image.name,
            "detections": [
                {
                    "class": row["name"],
                    "confidence": round(float(row["confidence"]), 4),
                    "bbox": [
                        round(float(row["xmin"]), 1),
                        round(float(row["ymin"]), 1),
                        round(float(row["xmax"]), 1),
                        round(float(row["ymax"]), 1),
                    ],
                }
                for _, row in detections.iterrows()
            ],
        })

    return summary


def print_yolo_summary(summary):
    for item in summary:
        detections = item["detections"]

        if not detections:
            print(f"{item['image']}: nenhuma detecção")
            continue

        found = ", ".join(
            f"{detection['class']} ({detection['confidence']:.2f})"
            for detection in detections
        )
        print(f"{item['image']}: {found}")


# ============================
# CNN
# ============================

def prepare_cnn_image(tf, image_path):
    # Reproduz o pré-processamento do notebook:
    # leitura RGB, redimensionamento para 128 x 128 e normalização entre 0 e 1.
    image = tf.io.read_file(str(image_path))
    image = tf.io.decode_image(image, channels=3, expand_animations=False)
    image.set_shape([None, None, 3])
    image = tf.image.resize(image, CNN_IMAGE_SIZE)
    image = tf.cast(image, tf.float32) / 255.0

    return image


def run_cnn(config, images):
    if not config["weights"].exists():
        raise FileNotFoundError(f"Modelo não encontrado: {config['weights']}")

    import tensorflow as tf

    model = tf.keras.models.load_model(str(config["weights"]))

    batch = tf.stack([prepare_cnn_image(tf, image) for image in images])
    probabilities = model.predict(batch, verbose=0)

    summary = []

    for image, image_probabilities in zip(images, probabilities):
        predicted_index = int(image_probabilities.argmax())

        predicted_class = CNN_CLASSES[predicted_index]
        expected_class = get_expected_class(image)

        summary.append({
            "image": image.name,
            "predicted_class": predicted_class,
            "expected_class": expected_class,
            "correct": (
                predicted_class == expected_class
                if expected_class else None
            ),
            "confidence": round(float(image_probabilities[predicted_index]), 4),
            "probabilities": {
                CNN_CLASSES[index]: round(float(value), 4)
                for index, value in enumerate(image_probabilities)
            },
        })

    return summary


def get_expected_class(image_path):
    name = image_path.stem.lower()

    for prefix, class_name in FILE_PREFIX_CLASSES.items():
        if name.startswith(prefix):
            return class_name

    return None


def save_cnn_images(results, images, output_dir):
    # A CNN classifica a imagem inteira (não localiza o objeto), então a
    # imagem anotada recebe uma faixa com a classe prevista e a confiança:
    # verde quando acerta, vermelha quando erra.
    from PIL import Image, ImageDraw, ImageFont

    output_dir.mkdir(parents=True, exist_ok=True)

    for item, image_path in zip(results, images):
        image = Image.open(image_path).convert("RGB")
        width, height = image.size

        banner_height = max(32, int(height * 0.09))
        margin = int(banner_height * 0.3)

        text = f"{item['predicted_class']} {item['confidence']:.2f}"

        if item["correct"] is not None:
            text += " | correto" if item["correct"] else (
                f" | esperado: {item['expected_class']}"
            )

        draw = ImageDraw.Draw(image)

        # Reduz a fonte até o texto caber na largura da imagem.
        font_size = int(banner_height * 0.55)

        while True:
            try:
                font = ImageFont.load_default(size=font_size)
            except TypeError:  # versões antigas do Pillow
                font = ImageFont.load_default()
                break

            if draw.textlength(text, font=font) <= width - 2 * margin or font_size <= 10:
                break

            font_size -= 2
        draw.rectangle(
            [(0, 0), (width, banner_height)],
            fill=BANNER_COLORS[item["correct"]],
        )
        draw.text(
            (margin, banner_height // 2),
            text,
            fill=(255, 255, 255),
            font=font,
            anchor="lm",
        )

        image.save(output_dir / image_path.name)


def print_cnn_summary(summary):
    for item in summary:
        status = ""

        if item["correct"] is not None:
            status = " - correto" if item["correct"] else (
                f" - incorreto (esperado: {item['expected_class']})"
            )

        print(
            f"{item['image']}: {item['predicted_class']} "
            f"({item['confidence']:.2f}){status}"
        )


# ============================
# EXECUÇÃO
# ============================

def run_vision(model_key, source=SAMPLES_DIR, confidence=0.25):
    """
    Executa o modelo escolhido e retorna o resumo das predições.
    Também salva o resumo em outputs/<modelo>/detections.json.
    """
    config = MODELS[model_key]
    images = collect_images(source)

    if not images:
        raise FileNotFoundError(f"Nenhuma imagem encontrada em: {source}")

    output_dir = OUTPUTS_DIR / model_key

    if config["type"] == "yolo":
        results = run_yolo(config, images, output_dir, confidence)
    else:
        results = run_cnn(config, images)
        save_cnn_images(results, images, output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "model": model_key,
        "model_label": config["label"],
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "confidence_threshold": confidence if config["type"] == "yolo" else None,
        "results": results,
    }

    with open(output_dir / "detections.json", "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)

    return summary, output_dir


def parse_arguments():
    parser = argparse.ArgumentParser(description="Visão computacional - Fase 6")

    parser.add_argument(
        "--model",
        choices=list(MODELS),
        default="yolo-60",
        help="Modelo utilizado (padrão: yolo-60).",
    )
    parser.add_argument(
        "--source",
        default=str(SAMPLES_DIR),
        help="Imagem ou pasta de imagens (padrão: samples).",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confiança mínima das detecções do YOLO (padrão: 0.25).",
    )

    return parser.parse_args()


def main():
    arguments = parse_arguments()
    config = MODELS[arguments.model]

    print(f"Modelo: {config['label']}")
    print(f"Imagens: {arguments.source}\n")

    try:
        summary, output_dir = run_vision(
            arguments.model,
            source=arguments.source,
            confidence=arguments.conf,
        )

    except ModuleNotFoundError as error:
        package = "tensorflow" if config["type"] == "cnn" else "torch"
        print(f"Dependência não instalada: {error.name}")
        print("Instale as dependências de visão: pip install -r requirements-vision.txt")
        print(f"(pacote principal deste modelo: {package})")
        return 1

    except FileNotFoundError as error:
        print(error)
        return 1

    print("\nResultados:")
    print("--------------------------------------")

    if config["type"] == "yolo":
        print_yolo_summary(summary["results"])
    else:
        print_cnn_summary(summary["results"])

    print(f"\nResultados salvos em: {output_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
