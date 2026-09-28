# Auricular Acupoint Detection Pipeline

A computer vision pipeline that locates 8 auricular (external ear) acupoints on standardised ear photographs, extracts colour and texture features at each point, and statistically compares those features across patient groups. It is built to test one open question: **do auricular points traditionally linked to hypertension and diabetes show a measurable, photograph-detectable signal?**

> **Status: work in progress.** The detection pipeline is built and validated on practice data. Real patient data collection (Healthy, Hypertension, Diabetes groups) is ongoing, so no diagnostic conclusions have been drawn yet.

---

## Research Question

Auricular acupuncture points for hypertension and diabetes are already used therapeutically, and trials show that stimulating them has clinical effects. What has not been tested is whether these points *look different* in people with the condition, using image analysis rather than touch or electrical measurement. Automated point detection exists, but it has not been connected to any disease-correlation study.

This project builds that connection, and is designed to report a null result as readily as a positive one.

## Target Points

Eight points, all visible from a front view of the ear:

| Point | Linked condition |
|---|---|
| EarApex | Hypertension |
| Endocrine | Hypertension and Diabetes |
| ShenMen | Hypertension and Diabetes |
| SuperiorTriangularFossa | Hypertension |
| Heart | Hypertension |
| Pancreas | Diabetes |
| Sympathetic | Diabetes |
| Kidney | Diabetes |

Point selection follows published auricular acupuncture literature (Kim et al., 2013 for hypertension; Suen et al., 2015 and related diabetes literature for diabetes). See References.

## Pipeline

```
Standardised ear photo
        |
LabelMe annotation (manual, training data only)
        |
YOLO11-pose keypoint detection  ->  8 point coordinates
        |
OpenCV feature extraction  ->  colour (RGB/HSV) + texture at each point
        |
scipy statistics  ->  t-test / ANOVA, Bonferroni-corrected
```

1. **Image acquisition:** fixed distance, lighting and framing (ring light, macro lens, tripod).
2. **Annotation:** the 8 points are labelled by hand in LabelMe to build training data.
3. **Detection:** a YOLO11-pose model is fine-tuned to predict all 8 points on new photos.
4. **Feature extraction:** a small patch around each detected point is measured for average colour and texture roughness.
5. **Statistical comparison:** independent t-tests for condition-specific points, one-way ANOVA for the two shared points, with a Bonferroni-corrected significance threshold.

## Repository Structure

```
.
├── README.md
├── .gitignore
└── scripts/
    ├── prepare_yolo_data.py   # LabelMe JSON -> YOLO format, automatic train/val split
    ├── data.yaml              # YOLO dataset config (8 keypoints)
    ├── train_yolo.py          # fine-tune YOLO11-pose
    ├── predict.py             # run the trained model on one image
    ├── extract_features.py    # colour/texture features at detected points
    └── compare_groups.py      # t-test / ANOVA across groups
```

## Setup

Python 3.10 or newer (developed on Python 3.14).

```bash
pip install ultralytics opencv-python scipy pandas matplotlib pillow labelme
```

## Usage

The dataset is not included (see Data and Ethics). To run the pipeline on your own images, create this layout next to `scripts/`:

```
data/
├── images/          # all raw photos, e.g. 01_L.jpg, 01_R.jpg
├── labelme_json/    # LabelMe annotations, one .json per image
└── labels/          # created automatically by prepare_yolo_data.py
```

**1. Annotate images in LabelMe**

```bash
python -m labelme data/images/ --output data/labelme_json/
```

Use these label names exactly, as the conversion script matches on them: `EarApex`, `Endocrine`, `ShenMen`, `SuperiorTriangularFossa`, `Heart`, `Pancreas`, `Sympathetic`, `Kidney`.

**2. Convert annotations and split into train/validation (80/20)**

```bash
cd scripts
python prepare_yolo_data.py
```

**3. Train**

```bash
python train_yolo.py
```

**4. Predict on a new image**

Edit `MODEL_PATH` and `IMAGE_PATH` in `predict.py`, then:

```bash
python predict.py
```

**5. Feature extraction and statistics**

`extract_features.py` and `compare_groups.py` run on detected points and group labels once patient data is available. `compare_groups.py` currently contains placeholder example values.

## Results So Far

Preliminary, from practice rounds ahead of real patient data:

| Round | Images | Pose mAP50-95 (validation) |
|---|---|---|
| Pilot | 4 (same images used for train and validation) | 0.00 |
| Round 1 | 50 (40 train / 10 val, 25 subjects) | 0.87 |
| Round 2 | 96 (77 train / 19 val, 48 subjects) | 0.93 |

Going from 4 to 50 images moved keypoint accuracy from zero to usable. Predictions shift from a collapsed cluster into the correct anatomical regions as data grows. Tested on ears unlike the training subjects, points are still placed less precisely than on validation images, which is the expected gap at this data scale.

## Limitations

- Small datasets, so validation metrics are noisy and likely optimistic.
- Left and right ears of the same subject can land in different splits, which can overstate accuracy. Future splits should be by subject.
- The correlation between point appearance and disease has **not been tested yet**. Nothing in this repository is a validated diagnostic method.
- Training subjects so far are not demographically diverse, which limits generalisation.

## Roadmap

- [x] End-to-end pipeline: annotation, detection, feature extraction, statistics
- [x] Scaling experiments (4 to 50 to 96 images)
- [x] Standardised image-acquisition protocol
- [ ] Complete Hypertension and Diabetes patient groups (30-40 per group)
- [ ] Retrain the detector on the full real dataset
- [ ] Run the statistical comparison across groups
- [ ] Report findings, whether or not a significant difference is found

## Data and Ethics

The dataset is **not included** in this repository because it consists of photographs of human subjects, and patient images collected for this study are confidential. The `.gitignore` excludes all image, annotation and model-weight folders. Collection follows informed consent and anonymised file naming.

## Disclaimer

This is a research prototype. It is not a medical device and must not be used to diagnose, screen for, or make decisions about any medical condition.

## References

1. J. H. Kim et al., "Auricular acupuncture for prehypertension and stage 1 hypertension: study protocol for a pilot multicentre randomised controlled trial," *Trials*, vol. 14, p. 303, 2013. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3848952/
2. L. K. P. Suen et al., "Association of Auricular Reflective Points and Status of Type 2 Diabetes Mellitus: A Matched Case-Control Study," *Evid. Based Complement. Alternat. Med.*, 2015. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4452325/
3. G. Wang et al., "A YOLOv11-based AI system for keypoint detection of auricular acupuncture points in traditional Chinese medicine," *Front. Physiol.*, vol. 16, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12287118/
