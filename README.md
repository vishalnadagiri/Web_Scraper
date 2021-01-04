# Web_Scraper
FlipKart web scraping of women's dress. And save the image of product to local directory

<br> with the present code one can extract the data of flipkart women's dresses and also save the product image to local directory
## list of details extracted 
```
['Product_name', 'Price', 'Didcount', 'P_URL', 'Rating', 'Color',
       'Length', 'Fabric', 'Pattern', 'Ideal For', 'Type', 'Style Code',
       'Suitable For', 'Sleeve Length', 'Pack of', 'Neck', 'Fabric Care',
       'Other Details', 'Sleeve', 'Generic Name', 'Country of Origin',
       'Description', 'P_Color', 'Avl_Color', 'Avl_Size', 'Image_path',
       'Lining Material']
       
 ```
<br> and further these data will be used to train the Auto Description model for a given image url the [model link](https://github.com/vishalnadagiri/AutoCaption/blob/main/AutoCaptionCNN_LSTM.ipynb)

Future Updates:
- using the data to train [Attr_model](https://github.com/vishalnadagiri/AutoCaption/blob/main/AutoCaption.ipynb) to predict the attributes of the images
