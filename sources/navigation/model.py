import tflite_runtime.interpreter as tflite
import numpy as np
import cv2


def load_model(path):
    interpreter = tflite.Interpreter(
        model_path=path,
        num_threads=8
    )
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    in_dtype = input_details[0]["dtype"]

    model_info = {
        "interpreter": interpreter,
        "input_details": input_details,
        "output_details": output_details,
        "is_int8": in_dtype == np.int8,
        "is_float": in_dtype == np.float32,
    }

    print("Input shape:", input_details[0]["shape"])
    print("Input dtype:", in_dtype)

    return model_info


def infer(model_info, model_img, resize_shape):
    interpreter = model_info["interpreter"]
    input_details = model_info["input_details"]
    output_details = model_info["output_details"]

    interpreter.set_tensor(input_details[0]["index"], model_img)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]["index"])

    if model_info["is_int8"]:
        out_scale, out_zero = output_details[0]["quantization"]
        logits = (output.astype(np.float32) - out_zero) * out_scale
    else:
        logits = output.astype(np.float32)

    logits = logits[0]

    if logits.shape[0] <= 10:
        mask = np.argmax(logits, axis=0)
    else:
        mask = np.argmax(logits, axis=-1)

    mask = cv2.resize(
        mask.astype(np.uint8),
        resize_shape,
        interpolation=cv2.INTER_NEAREST
    )

    return mask