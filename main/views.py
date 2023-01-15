from fileinput import filename
from django.shortcuts import render
from django.shortcuts import render, redirect
from subprocess import run, PIPE
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from zipfile import ZIP_DEFLATED

import pandas as pd
import sys
import os
import logging
import shutil
# from pyrsistent import T
logger = logging.getLogger(__name__)
from datetime import datetime



def login_page(request):
    if(request.user.is_authenticated):
        return redirect('index')
    else:
        if request.method =='POST':
            username = request.POST.get("user")
            password = request.POST.get("pass")
            user = authenticate(username=username, password=password)      

            if user is not None and user.groups.filter(name__in=['data', 'marketing', 'platform', 'accounts', 'rides','food', 'cx']).exists():
                login(request, user)
                return redirect('index')
            else:
                return render(request, "login.html", {"error":True})
        return render(request, "login.html")


def opening_page(request):
    return render(request, "opening_page.html")
      
def index(request):     
    context = {
        "videos" : ['world','programmer','animation','stick'],
    }
    return render(request, "index.html", context)

def not_found(request):
    return render(request, "not_found.html")
    


def get_info(request):
    if request.method =='POST' and'get_info' in request.POST:
       
        # else input the file and process process further	
            my_uploaded_file = request.FILES['file1']
            
            base_dir = os.path.abspath('.')
            try:
                user_folder = os.path.join(base_dir+'/main/static/result/get_info/' + str(request.user.username)+'/')
            except:
                os.makedirs(os.path.join(base_dir+'/main/static/result/get_info/' + str(request.user.username)+'/'))
                user_folder = os.path.join(base_dir+'/main/static/result/get_info/' + str(request.user.username)+'/')

            # if user folder already present then replace them with new files 
            if os.path.exists(user_folder):
                filelist = [ f for f in os.listdir(user_folder) ]
                
                for f in filelist:
                    os.remove(os.path.join(user_folder, f))
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            
            sys.path.append('..')

            
            # save the input file temporarily and pass it to the jupyter file and return the final html
            from scripts.save_csv import conv_csv
            conv_csv(my_uploaded_file,user_folder)
            

            from scripts.get_info import final_func
            result = final_func(user_folder+'data.csv')

            
            return render(request, "get_info.html" ,{'r':True})

    return render(request, "get_info.html")



def analyze_data(request):
    if request.method =='POST' and'get_html' in request.POST:
        user_ = str(request.user.username)
        my_uploaded_file = request.FILES['file1']	
        base_dir = os.path.abspath('.')
            
        try:
            user_folder = os.path.join(base_dir+'/main/static/result/analyze_data/'+str(request.user.username)+'/')
                
        except:
            os.makedirs(os.path.join(base_dir+'/main/static/result/analyze_data/'+str(request.user.username)+'/'))
   
        notebook_path = os.path.join(base_dir+'/script/')

        if os.path.exists(user_folder):
                filelist = [ f for f in os.listdir(user_folder) ]
                for f in filelist:
                    os.remove(os.path.join(user_folder, f))
        if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            
        sys.path.append('..')

        from scripts.save_csv import conv_csv
        conv_csv(my_uploaded_file,user_folder)
        
        from scripts.exec_jupyter import final_func	
        source = notebook_path + "rfm_project.ipynb"
        destination  = user_folder+'rfm_project.ipynb'
        shutil.copy(source, destination)	
        from scripts.exec_jupyter import final_func
        result = final_func(destination,user_)

        with open(user_folder +"analyze_data.html", "w") as f:
            f.write(result)
                
        return render(request, 'analyze_data.html',{'r':True})

    return render(request, "analyze_data.html")



def test_data(request):
    base_dir = os.path.abspath('')
    user_folder = os.path.join(base_dir+'/main/static/result/get_info/' + str(request.user.username))
    from scripts.get_info import final_func
    result = final_func(user_folder+'/data.csv')
    print("selected id is ")
    if request.method =='POST'and'final_info' in request.POST:	
        print("final info on the way")
        selected_id = request.POST.get('selected_c_id')
        print("selected id is ", selected_id)
        data_folder = os.path.join(base_dir+'/main/static/result/get_info/' + str(request.user.username)+'/data.csv')
        # return render(request, "final_info.html",{'r':True, 'ready': selected_id}) 
        from scripts.get_info import info_func
        output = info_func(user_folder+'/data.csv',selected_id)
        print("Output as ", output)
        return render(request, "test.html",{'p':True, 'res': output, 'customer_id': selected_id})
    return render(request, "test.html",{'r':True, 'ready': result})

