# Checkup - Project Log

## [05.07] Project starts today!
 - [x] Creat a __crawler__ to get multiple imgs by key word '`体检单`' in [Baidu Image](https://image.baidu.com/).
 - [x] Add filter to my crawler to ignore _low resolution pics_ & _expired urls_ .
 - [x] Using [Baidu OCR](https://ai.baidu.com/) to recognize texts in images.
 - [ ] Optimize OCR procedure with [`multiprocessing`](https://docs.python.org/3.6/library/multiprocessing.html) library.
 - [ ] Correct the direction of downloaded image, reproduced the font size according to [Baidu OCR](https://ai.baidu.com/) api response.

 ![achv-0507](./achv/achv-0507.png)

---

## [05.08] Code review & Optimization
 - [x] Extend my __crawler__ to support multiple key words, and test it to download larger amount of pictures (`627` valid / `2300` in total).
 - [x] Add `isDownloaded` check to my crawler to skip downloaded pictures.
 - [ ] (More TODOs coming up...)
