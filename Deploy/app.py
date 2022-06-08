from flask import Flask,render_template,request
import os
import logging
import results

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

app=Flask(__name__, static_url_path='/static')

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/',methods=['POST', 'GET'])
def submit():
    logging.info("done")

    image = request.files["img"]
    name= image.filename
    mainimage = f'static/requested_images/{name}'
    scale = request.form['scale']
    
    for file in os.listdir('static/requested_images'):
        os.remove(f'static/requested_images/{file}')
    image.save(f'static/requested_images/{name}')

    
    seg_image, cropped, labels, areas, panels = results.get_Predictions(mainimage, scale)

    # cropped = ['static/crop/1.jpg', 'static/crop/4.jpg', 'static/crop/2.jpg', 'static/crop/3.jpg']
    # labels = ['Hip', 'Hip', 'Flat', 'Flat'] 
    # areas = [64.8, 2.32, 18.9, 117.38]
    # panels = ['static/panels/1.jpg', 'static/panels/4.jpg', 'static/panels/2.jpg', 'static/panels/3.jpg']
    # seg_image = 'static/segmented_images/1.png'

    return render_template('index.html',image=mainimage, seg_img = seg_image, cropped = cropped, labels=labels, area = areas, panels=panels) 

    
if __name__=='__main__':
    port = os.environ.get("PORT",5000)
    app.run(debug=False,host='0.0.0.0',port=port)
