============================================================
LuSNAR Segmentation Model - TFLite Deployment Notes
============================================================

Project:
  Semantic segmentation model trained on LuSNAR Moon dataset scenes.

Architecture:
  UNetMobileNet (PyTorch)

Model Output:
  Per-pixel classification into 5 classes.

------------------------------------------------------------
1) CLASSES / LABELS
------------------------------------------------------------

Class IDs:
  0 = Regolith
  1 = Crater
  2 = Rock
  3 = Mountain
  4 = Sky

Color Map (RGB) used for visualization:
  0 -> (187,  70, 156)   Regolith
  1 -> (120,   0, 200)   Crater
  2 -> (232, 250,  80)   Rock
  3 -> (173,  69,  31)   Mountain
  4 -> ( 34, 201, 248)   Sky

------------------------------------------------------------
2) INPUT PREPROCESSING (VERY IMPORTANT)
------------------------------------------------------------

CRITICAL NOTE:
  This model was trained WITHOUT ImageNet normalization.

During training, images were loaded using:
  torchvision.transforms.functional.to_tensor()

Meaning:
  - RGB input
  - float32
  - range [0, 1]
  - NO (x - mean) / std normalization

Correct preprocessing:
  img_float = img_uint8.astype(float32) / 255.0

DO NOT APPLY ImageNet normalization:
  (x - mean) / std

If ImageNet normalization is applied, predictions will become incorrect.

------------------------------------------------------------
3) MODEL INPUT / OUTPUT FORMAT
------------------------------------------------------------

Input tensor:
  Layout: NCHW
  Shape:  (1, 3, H, W)
  Dtype:  float32 (FP32/FP16 models)
  Range:  [0, 1]

Example:
  (1, 3, 384, 384)

Output tensor:
  Layout: NCHW
  Shape:  (1, 5, H, W)
  Output is LOGITS (not softmax probabilities)

To obtain segmentation mask:
  mask = argmax(output[0], axis=0)

------------------------------------------------------------
4) IMAGE RESOLUTION (TRAINING / DEPLOYMENT)
------------------------------------------------------------

Training resolution:
  - The model was trained using images resized to 384x384.

Deployment resolution:
  - The exported ONNX/TFLite models expect fixed input size 384x384.

Pixel value scaling:
  - Input images are expected as float32 in range [0,1].
  - If the image is loaded as uint8 [0..255], convert using:

        img_float = img_uint8.astype(float32) / 255.0

IMPORTANT:
  "255" refers ONLY to pixel intensity range conversion, not image resolution.

------------------------------------------------------------
5) EXPORT / CONVERSION PIPELINES
------------------------------------------------------------

Pipeline used:
  PyTorch (.pth) -> ONNX -> SavedModel (onnx-tf) -> TFLite

Files produced:
  outputs/model.onnx
  outputs/model_simplified.onnx
  outputs/model_tf/               (TensorFlow SavedModel directory)
  outputs/model_fp16.tflite
  outputs/model_int8.tflite
  outputs/segmentation_preview_*.png

------------------------------------------------------------
6) FP16 MODEL DETAILS
------------------------------------------------------------

File:
  outputs/model_fp16.tflite

Quantization type:
  FP16 weight quantization

Notes:
  - Weights stored as float16
  - Input tensor remains float32
  - Output tensor remains float32
  - No calibration dataset required

------------------------------------------------------------
7) INT8 MODEL DETAILS
------------------------------------------------------------

File:
  outputs/model_int8.tflite

Quantization type:
  Full integer quantization (INT8)

Calibration:
  Uses representative dataset samples (float32 input in [0,1])

IMPORTANT:
  Representative dataset MUST use the SAME preprocessing as training:
    - float32
    - range [0,1]
    - no ImageNet normalization

Inference:
  Input and output tensors are int8.
  Must quantize input and dequantize output using scale/zero_point.

------------------------------------------------------------
8) TFLITE INFERENCE (FP32 / FP16)
------------------------------------------------------------

Example (Python):

  interpreter = tf.lite.Interpreter(model_path="model_fp16.tflite")
  interpreter.allocate_tensors()

  inp = interpreter.get_input_details()[0]
  out = interpreter.get_output_details()[0]

  # image_float must be float32 [0,1] with shape (3,H,W)
  input_data = np.expand_dims(image_float, axis=0).astype(np.float32)

  interpreter.set_tensor(inp["index"], input_data)
  interpreter.invoke()

  logits = interpreter.get_tensor(out["index"])    # (1,5,H,W)
  mask   = np.argmax(logits[0], axis=0).astype(np.uint8)

------------------------------------------------------------
9) TFLITE INFERENCE (INT8)
------------------------------------------------------------

Example (Python):

  interpreter = tf.lite.Interpreter(model_path="model_int8.tflite")
  interpreter.allocate_tensors()

  inp = interpreter.get_input_details()[0]
  out = interpreter.get_output_details()[0]

  in_scale,  in_zero  = inp["quantization"]
  out_scale, out_zero = out["quantization"]

  input_float = np.expand_dims(image_float, axis=0).astype(np.float32)

  # Quantize float32 -> int8
  input_int8 = np.round(input_float / in_scale + in_zero)
  input_int8 = np.clip(input_int8, -128, 127).astype(np.int8)

  interpreter.set_tensor(inp["index"], input_int8)
  interpreter.invoke()

  output_int8 = interpreter.get_tensor(out["index"])

  # Dequantize int8 -> float32 logits
  logits = (output_int8.astype(np.float32) - out_zero) * out_scale

  mask = np.argmax(logits[0], axis=0).astype(np.uint8)

------------------------------------------------------------
10) COMMON PITFALLS
------------------------------------------------------------

(1) WRONG NORMALIZATION
  - The model expects [0,1] input.
  - Do NOT apply ImageNet mean/std normalization.

(2) NCHW vs NHWC
  - This model uses NCHW.
  - Always check tensor shapes in TFLite:

      print(inp["shape"])
      print(out["shape"])

  Expected:
      input:  (1,3,H,W)
      output: (1,5,H,W)

(3) MISSING CLASSES IN PREDICTION
  - Some images do not contain all 5 classes.
  - It is normal that np.unique(mask) returns only a subset.

------------------------------------------------------------
11) DEBUGGING CHECKLIST
------------------------------------------------------------

If predictions look wrong:

  1) Verify preprocessing:
       - float32
       - RGB
       - divide by 255.0
       - no normalization

  2) Print tensor details:
       print(inp)
       print(out)

  3) Print output range:
       print(logits.min(), logits.max())

  4) Compare a single pixel logits against PyTorch output.

------------------------------------------------------------
12) PERFORMANCE NOTES (Raspberry Pi / CPU)
------------------------------------------------------------

- FP16 weights may not speed up inference on CPU-only devices.
- INT8 typically provides the best speedup on Raspberry Pi (if int8 ops are optimized).

------------------------------------------------------------
END OF FILE
============================================================
