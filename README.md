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
 - [to-do] Manually orting download images into two class of _report_ (?/627) or _notReport_ (?/627).
 - [DONE] Learn basics about __image classifier__ with Tensorflow. Some materials are listed below:
   - [TensorFlow Tutorial 2: Image Classification Walk-through](https://www.youtube.com/watch?v=oXpsAiSajE0)
   - [Train an Image Classifier with TensorFlow for Poets - Machine Learning Recipes #6](https://www.youtube.com/watch?v=cSKfRcEDGUs)
   - [Easy Image Classification with Tensorflow](https://www.youtube.com/watch?v=qaQofXTxkSo)
   - [Build a TensorFlow Image Classifier in 5 Min](https://www.youtube.com/watch?v=QfNvhPx5Px8)
 - [to-do] Extract words from '_report_' images and find some pattern (IDEA! The _is_Report_ detection can use both image classifier & context classifier).
 - [to-do] Use [opencv-python](https://pypi.org/project/opencv-python/) library and [Baidu OCR](https://ai.baidu.com/) to optimize image (lightness / direction / contrast / white balance).
