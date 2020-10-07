from django.shortcuts import render, redirect

# Create your views here.

from .models import Note

def notepad(request):
	#get note or show up like new Note
	noteid = int(request.GET.get('noteid',0))  
	#read all notes
	notes = Note.objects.all()
	
	
	# if SAVE is clicked to submit
	if request.method == 'POST':
		noteid_sub = int(request.POST.get('noteid', 0))
		name_sub = request.POST.get('name')
		datas_sub = request.POST.get('content', '')
		
		if noteid_sub > 0:
			#need to update existing
			notepage = Note.objects.get(pk=noteid_sub)
			notepage.name = name_sub
			notepage.datas = datas_sub
			notepage.save()
			#update webpage with new saved info (refreshed from DB)
			return redirect('/notes?noteid=%i' %noteid_sub)
		else:
			#new note need to be added
			notepage = Note.objects.create(name=name_sub, datas=datas_sub)
			#update webpage with new note from DB
			return redirect('/notes?noteid=%i' %notepage.id)
			
		
	
	
	
	# if existing note, point to that note id in DB
	if noteid > 0:
		notepage = Note.objects.get(pk=noteid)
	else:
		notepage = ''
	
	
	
	
	book = {
		'noteid': noteid,
		'notes': notes,
		'notepage' : notepage
		}
		
	return render(request, 'notepad.html', book)



def del_note(request, noteid):
	notepage = Note.objects.get(pk=noteid)
	notepage.delete()
	#refresh webpage and open empty note
	return redirect('/notes?noteid=0')
