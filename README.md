# SocioPath

The task is to develop an adaptive framework which automatically extracts information on local event announcements (e.g., concerts, lectures, festivals, performances etc.) from a webpage. 

### The primary results of this thesis 

* We made a review of existing modern Web Extraction methods, considered all main complementary tasks and listed work related to social events extraction. 

* We developed the original system which in parallel collects training examples for an event extraction problem with the use of Microdata semantic markup.

* Hence, we automatically created the training labeled dataset which contains various web features: visual, textual, spatial and DOM-related.

* We performed extensive cleaning procedure on the original dataset what reduced the number of records and columns dramatically.

* We engineered many features from original ones.

* We made comprehensive exploratory data analysis for every event component including visualization of extracted features and their relationships, dimensionality reduction and clustering.

* We built several binary classification models for every event component and calculated the primary performance metrics. We got the high performance metrics for all event components thanks to set of relevant features, calculating the tf-idf matrix and PCA dimensionality reduction.

* We made the final dataset public and therefore it is the first publicly available dataset for social event extraction problem. The data with the code are available in this GitHub repository (DATA_FINAL.zip)


The main conclusion of the thesis is also that we demonstrated that it is possible to automatically extract training dataset, prepare and build meaningful models which can recognize the event components on a web page. The list of items annotated with the semantic markup is very large, and hypothetically our approach can be extended to any of them. 


### References:

[1] John Foley, Michael Bendersky, Vanja Josifovski. "Learning to Extract Local Events from the Web". SIGIR 2015, 2015

[2] Nikolaos Pappas, Georgios Katsimpras, Efstathios Stamatatos. "Extracting Informative Textual Parts from Web Pages Containing User-Generated Content". 12th Int. Conference on Knowledge Management and Knowledge Technologies, Graz, Austria, 2012 

[6] Alberto H. F. Laender, Berthier A. Ribeiro-Neto, Altigran S. da Silva, Juliana S. Teixeira. "A Brief Survey of Web Data Extraction Tools"; ACM SIGMOD Record, Volume 31 Issue 2, June 2002

[4] Gengxin Miao, Junichi Tatemura, Wang-Pin Hsiung. "Extracting Data Records from the Web Using Tag Path Clustering". Proceedings of the 18th international conference on World wide web, Pages 981-990, 2009

[5] Xuan-Hieu Phan, Susumu Horiguchi, Tu-Bao Ho. "Automated data extraction from the web with conditional models". International Journal of Business Intelligence and Data Mining archive, Volume 1 Issue 2, 2005 
