# PUP
This repo contains datas and model to Allcart product categorization. The model was developed with more than 300K products in the following categories:
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
