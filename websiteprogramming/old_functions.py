import os


# with architecture teseting
def get_archfiles_lists():
    archpath='/Users/shalevwiden/Downloads/Projects/degreeview/School of Architecture'

    csvlist=[]
    excellist=[]
    pdflist=[]
    mmdlist=[]
    # os.walk recursively travels everything
    for root, dirs, files in os.walk(archpath):
        for file in files:
            
            # we neewd the fullpath in the list since thats the way it can be uploaded to google cloud.

            full_path = os.path.join(root, file)

            if os.path.splitext(file)[1]=='.csv':
                csvlist.append(file)
                # removes those dollar sign excel files. 
            elif os.path.splitext(file)[1]=='.xlsx' and not file.startswith(("~$", "$")):
                excellist.append(full_path)
            elif os.path.splitext(file)[1]=='.pdf':
                pdflist.append(file)
            elif os.path.splitext(file)[1]=='.mmd':
                mmdlist.append(file)

    return excellist

print('Printing all excel files in arch folder ')
for i in get_archfiles_lists():
    print(i+'\n')