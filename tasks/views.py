from tasks.forms import ZipForm
from tasks.models import Task, TaskFile
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, response, FileResponse
from django.utils import timezone
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import mimetypes

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'tasks/index.html'
    context_object_name = "taskList"
    
    def get_queryset(self):
        return Task.objects.filter( deleted=False ).order_by('upload_date')

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "tasks/detail.html"
    
@login_required
def new_task(request):
    form = ZipForm()

    context={'form':form}

    return render(request, 'tasks/new.html', context)

@login_required
def book(request, task_id):

    try:        
        bookedTask = get_object_or_404(Task, pk=task_id)
        username = ""
        if request.user.is_authenticated:
            username = request.user.username

        bookedTask.booked_by = username
        bookedTask.save()

    except (KeyError, Task.DoesNotExist):
        return render(request, 'tasks/index.html', {
            "error_message": "Error occured"
        })

    return render(request, 'tasks/book.html', {
        "username": username
    })

@login_required
def download(request, task_id):

    try:        
        downloadTask = get_object_or_404(Task, pk=task_id)
        username = ""
        if request.user.is_authenticated:
            username = request.user.username

        if username == downloadTask.booked_by:
            
            downloadTaskFile = get_object_or_404(TaskFile, task=downloadTask)
            fl_path = downloadTaskFile.zip_file.path
            response = FileResponse(open(fl_path, 'rb'))

            return response
        else:
            return render(request, 'tasks/no_perm.html', {
                "error_message": "You don't have permission to download this file."
            })

    except (KeyError, Task.DoesNotExist):
        return render(request, 'tasks/index.html', {
            "error_message": "Error occured"
        })

@login_required
def revoke(request, task_id):

    try:        
        revokedTask = get_object_or_404(Task, pk=task_id)

        username = ""
        if request.user.is_authenticated:
            username = request.user.username

        if username == revokedTask.booked_by:
            revokedTask.booked_by = ""
            revokedTask.save()
        else:
            return render(request, 'tasks/no_perm.html', {
                "error_message": "You don't have permission to revoke"
            })

    except (KeyError, Task.DoesNotExist):
        return render(request, 'tasks/index.html', {
            "error_message": "Error occured"
        })

    return render(request, 'tasks/revoke.html')

@login_required
def delete(request, task_id):
    try:        
        deletedTask = get_object_or_404(Task, pk=task_id)

        username = ""
        if request.user.is_authenticated:
            username = request.user.username

        if username == deletedTask.booked_by:
            deletedTask.deleted = True
            deletedTask.save()
        else:
            return render(request, 'tasks/no_perm.html', {
                "error_message": "You don't have permission to delete files you haven't booked."
            })

    except (KeyError, Task.DoesNotExist):
        return render(request, 'tasks/index.html', {
            "error_message": "Error occured"
        })

    return render(request, 'tasks/delete.html')

@login_required
def new_task_success(request):
    newTaskTitle = ""
    try:        
        form = ZipForm(request.POST, request.FILES)
        if form.is_valid():

            uploadedFile=request.FILES['zip_file']
            
            if uploadedFile.name[-4:] == ".zip":

                newTaskTitle = request.POST['title']
                newTask = Task(title=newTaskTitle, upload_date=timezone.now(), deleted=False)
                newTask.save()

                newTaskZip = TaskFile(task=newTask, zip_file=uploadedFile)
                newTaskZip.save()
            else:
                return render(request, 'tasks/no_perm.html', {
                    "error_message": "You have to upload a zip file."
                })

    except (KeyError):
        return render(request, 'tasks/new.html', {
            "error_message": "Error occured"
        })
    
    return render(request, 'tasks/new_success.html', {
        "newTaskTitle": newTaskTitle
    })
