# Ear Acupoint Pipeline - v2 (Real-Scale Round)

Upgraded from the 4-photo practice round. Two real changes:
1. Proper train/val split (previously used the same 4 photos for both - misleading)
2. More training epochs (150 vs 50), since there's more to actually learn now

## IMPORTANT: clarify what these 25 subjects are for, before you start

- If this batch will feed into your real hypertension/diabetes correlation study,
  you need each subject's CONFIRMED DIAGNOSIS recorded (healthy / hypertension / diabetes),
  linked to an anonymized patient ID - not just the photos alone.
- If this batch is purely to improve the acupoint DETECTION model before real
  patient groups arrive, no diagnosis needed - any 25 people work fine.
- Either way, keep photos from the SAME person's left and right ear clearly
  paired to that person's ID (e.g. `P001_L.jpg`, `P001_R.jpg`), in case you want to
  analyze left/right separately later.

## Workflow

### 1. Put ALL your raw photos directly in `data/images/`
Not in train/ or val/ subfolders yet - just drop all 50 photos here first.
Use consistent naming: `P001_L.jpg`, `P001_R.jpg`, `P002_L.jpg`, etc.

### 2. Label every photo with LabelMe
```
labelme data/images/ --output data/labelme_json/ --nodata
```
Label all 8 points (EarApex, Endocrine, ShenMen, SuperiorTriangularFossa, Heart,
Pancreas, Sympathetic, Kidney) on every photo - exact spelling matters.

### 3. Run the conversion + auto-split script
```
cd scripts
python prepare_yolo_data.py
```
This automatically splits your labeled photos ~80/20 into `data/images/train`,
`data/images/val` (and matching `data/labels/train`, `data/labels/val`), copying
files into place. With 50 photos, expect roughly 40 train / 10 val.

### 4. Train
```
python train_yolo.py
```
Takes longer than the practice round (150 epochs, more images) - expect several
minutes rather than under a minute.

### 5. Check results.png
Look specifically at `metrics/mAP50(P)` (Pose accuracy) in the bottom-right area -
it should show SOME improvement over training, unlike the flat zero from 4 photos.
Still won't be "production accurate" at 50 images, but this is where you should
start seeing real signal.

## What comes after this round

Even at 50 images, real accuracy is still limited (Wang et al. 2025's benchmark
paper used 660 images). This round is a genuine step forward from practice, but
your actual 90-120 image target (30-40 per group x 3 groups) is still where you're
headed for the real study - keep collecting after this batch, don't treat 50 as
the finish line.
