# PUP (Product User Profile)
<img src="https://img.shields.io/badge/99.8%25-ACCURACY-yellow" /> <img src="https://img.shields.io/badge/82.8%25-ROC AUC-green" /><br>
![GOOGLE CLOUD](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![COLAB](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252)
![JSON](https://img.shields.io/badge/json-5E5C5C?style=for-the-badge&logo=json&logoColor=white)
![NUMPY](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![PANDAS](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![PYTHON](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![SCIKIT LEARN](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![UBUNTU](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
<br>
## Dependencies
<img src="https://img.shields.io/badge/PYTHON-3.0.7-red" /> <img src="https://img.shields.io/badge/PANDAS-1.1.4-green" /> <img src="https://img.shields.io/badge/JOBLIB-1.1.0-yellowgreen" /> <img src="https://img.shields.io/badge/NLTK-3.7.0-blue" /> <img src="https://img.shields.io/badge/SCIKIT LEARN-1.1.2-orange" /><br>
## Purpose
The model was developed to classify groceries, personal care and household supply products from any store accordingly to its name. The dataset used had more than 300K products in the following categories:
- Health Care
- Vitamins & Dietary Supplements
- Personal Care 
- Baby & Child Care 
- Hair Care
- Laundry Supplies 
- Household Supplies 
- Paper & Plastic Household Supplies 
- Facial Skin Care
- Eye Care  
- Body Cleansers  
- Oral Care  
- Household Cleaning 
- Shave & Hair Removal   
- Skin Care

## Usage
1 - Download the git repository and set it in the same script folder.<br>
2 - Import it as a package:<br>
  > from PUP.cats import CAT<br>

3 - Call the function:<br>
  > CAT("Yoplait Go-Gurt Simple Low Fat Yogurt, Variety, 2.25 oz, 32-count")<br>

4 - Output: list(str,str)
  > ['Dairy, Cheese & Eggs','Yogurt']
