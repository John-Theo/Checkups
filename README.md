# Checkup - Project Log

## [05.07] Project starts today!
 - [DONE] Creat a __crawler__ to get multiple imgs by key word '`体检单`' in [Baidu Image](https://image.baidu.com/).
 - [DONE] Add filter to my crawler to ignore _low resolution pics_ & _expired urls_ .
 - [DONE] Using [Baidu OCR](https://ai.baidu.com/) to recognize texts in images.
 - [to-do] Optimize OCR procedure with [`multiprocessing`](https://docs.python.org/3.6/library/multiprocessing.html) library.
 - [to-do] Correct the direction of downloaded image, reproduced the font size according to [Baidu OCR](https://ai.baidu.com/) api response.

![achv-0507](./achv/achv-0507.png)

---

## [05.08] Code review & Optimization
 - [DONE] Extend my __crawler__ to support multiple key words, and test it to download larger amount of pictures (`627` valid / `2300` in total).
 - [DONE] Add `isDownloaded` check to my crawler to skip downloaded pictures.
 - [DONE] Speed up OCR procedure with [`multiprocessing`](https://docs.python.org/3.6/library/multiprocessing.html) library.
 - [to-do] Correct the direction & lightness of images for model training later.
 
![achv-0508](./achv/achv-0508.png)
 
 ---
 
 ## [05.09] Data cleaning and tagging
 - [to-do] Manually orting download images into two class of _report_ (218/627) or _notReport_ (409/627).
 - [DONE] Learn basics about __image classifier__ with Tensorflow. Some materials are listed below:
   - [TensorFlow Tutorial 2: Image Classification Walk-through](https://www.youtube.com/watch?v=oXpsAiSajE0)
   - [Train an Image Classifier with TensorFlow for Poets - Machine Learning Recipes #6](https://www.youtube.com/watch?v=cSKfRcEDGUs)
   - [Easy Image Classification with Tensorflow](https://www.youtube.com/watch?v=qaQofXTxkSo)
   - [Build a TensorFlow Image Classifier in 5 Min](https://www.youtube.com/watch?v=QfNvhPx5Px8)
 - [to-do] Extract words from '_report_' images and find some pattern (IDEA! The _is_Report_ detection can use both image classifier & context classifier).
 - [to-do] Use [opencv-python](https://pypi.org/project/opencv-python/) library and [Baidu OCR](https://ai.baidu.com/) to optimize image (lightness / direction / contrast / white balance).
 - [FAIL] Multiprocess dead with no reason, DISABLE multiprocess functionality.

![achv-0509](./achv/achv-0509.png)
 
---

## [05.10-05.12] Batching OCR / Text extracting
 - [DONE] OCR every image, save synthetic image for future debuging, save image for text classification.
 - [to-do] How to isolate our interested area and auto-correct incorrect character in OCR result?

![achv-0510](./achv/achv-0510.png)
![achv-0510-2](./achv/achv-0510-2.png)

---

## [05.11-05.12] (Progress stagnated)
 - Perparing for [_China College Students' Enterpreneurship Competition 2018_](http://www.chuangqingchun.net/)
 - Coding for [_KDD CUP 2018_](https://biendata.com/competition/kdd_2018/)

![achv-0511](./achv/KDD.jpg)
![achv-0512](./achv/cqc.png)

---

## [05.13] Model choosing for image classification
 - [DONE] Choose [Tensorflow for Poets](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0) for __Image Classification__
 - [DONE] Decided to use both image classification and text classification to distinguish whether a target image is a checkup report or not.
 - [to-do] Choose a text classfier
 - [to-do] Deciede how much categories should there be to improve classification result. (`is_report`/`paper_but_not_report`/`not_paper`)

![achv-0513](./achv/achv-0513.png)
