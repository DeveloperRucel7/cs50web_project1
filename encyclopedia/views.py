import random
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
from . import util


def convert_md_html(title):
    content = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request,title):
    html_content = convert_md_html(title) 
    if html_content ==None:
        return render(request, 'encyclopedia/error.html',{
            "error_message":f"The Content of the {title} page is not available for the moment",
            "title":title
        })
    else:
        return render(request, 'encyclopedia/entries.html',{
            "content":html_content,
            "title":title,
        })

def search(request):
    if request.method == "POST":
        word = request.POST['q']
        result_search = convert_md_html(word)
       
        if result_search != None:
            return render(request, 'encyclopedia/entries.html',{
                "content":result_search,
                "title":word,
            })
        else:
            Entries = util.list_entries()
            results = []
            for entry in Entries:
                if word.lower() in entry.lower():
                    results.append(entry)
            return render(request, 'encyclopedia/search.html',{
                "results":results,

            })
    return render(request, 'encyclopedia/index.html')

def add_page(request):
    if request.method== "GET":
        return render(request, 'encyclopedia/add_page.html')
    else:
        title = request.POST['title']
        content  = request.POST["content"]
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html",{
                "error_message":"Oops!  The Title already exist. Please choose the another one",
                "title":title,
            })
        else:
            util.save_entry(title,content)
            html_content = convert_md_html(title)
            return render(request, 'encyclopedia/entries.html',{
            "content":html_content,
            "title":title,
        })
    
def edit_page(request):
    if request.method =="POST":
        title = request.POST['edit_title']
        content = util.get_entry(title)
    return render(request, 'encyclopedia/edit_page.html',{
        "title":title,
        "content":content,
    })

def save_page(request):
    if request.method =="POST":
        new_title = request.POST['edit_title']
        new_content = request.POST['edit_content']
        if new_content != '' and  new_title !='':
            util.save_entry(new_title,new_content)
            content = convert_md_html(new_title)
            return render(request, 'encyclopedia/entries.html',{
            "content":content,
            "title":new_title,
            })
        else:
            return render(request, 'encyclopedia/error.html',{
                "error_message":"Oops!  Please fill the Form completly",
            })

def random_page(request):
    random_pages = util.list_entries()
    random_page = random.choice(random_pages)
    content = convert_md_html(random_page)
  
    return render(request, 'encyclopedia/random.html',{
        "title":random_page,
        "content":content,
    })

    