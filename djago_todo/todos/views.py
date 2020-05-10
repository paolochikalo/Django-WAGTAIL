from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import ToDo


def list_todo_items(request):
    context = {'todo_list': ToDo.objects.all()}
    return render(request, 'todos/todo_list.html', context)

def insert_todo_item(request:HttpRequest):
    #content --> name of the html element: <input type="text" class="form-control"...
    todo = ToDo(content = request.POST['content'])
    todo.save()
    return redirect('/list/')

def delete_todo_item(request, todo_id):
    todo_id_delete = ToDo.objects.get(id=todo_id)
    todo_id_delete.delete()
    return redirect('/list/')

