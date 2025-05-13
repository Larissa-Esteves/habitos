from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Habito
from django.contrib.auth.views import LoginView

# forçar o login
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('listar-habito')  # força redirecionamento

# página index  
def index(request):
    return render(request, 'index.html')

# Cria uma subclasse para o form padrão do django
class CustomUserCreationForm(UserCreationForm):

    # a função garante que o form funcione e customiza os campos 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Percorre os campos do form, add o css e estiliza o bootstrap
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# redireciona o usuário para cadastrar seu login
def registrar(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('listar-habito')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

# Lista apenas os usuários logados
class HabitoListView(LoginRequiredMixin, ListView):
    model = Habito
    template_name = 'habitos/habitos.html' # caminho do template
    context_object_name = 'habitos' # nome usado no template para acessar a lista

    def get_queryset(self):
        # Retorna os hábitos do usuário logado
        return Habito.objects.filter(usuario=self.request.user)

# Formulário para criar um hábito
class HabitoCreateView(LoginRequiredMixin, CreateView):
    model = Habito
    fields = ['nome', 'descricao']
    template_name = 'habitos/habito_form.html'
    success_url = reverse_lazy('listar-habito') # redireciona após criado

    def form_valid(self, form):
        form.instance.usuario = self.request.user # associa um hábito ao usuaŕio logado
        return super().form_valid(form)
    
# Detalhes do hábito
class HabitoDetailView(LoginRequiredMixin, DetailView):
    model = Habito
    template_name = "habitos/habito_detail.html"

# altera os hábitos registrados
class HabitoUpdateView(LoginRequiredMixin, UpdateView):
    model = Habito
    fields = ['nome', 'descricao']
    template_name = 'habitos/habito_form.html'  # Pode reutilizar o mesmo template
    success_url = reverse_lazy('listar-habito')

    def get_queryset(self):
        # Garante que o usuário só edite seus próprios hábitos
        return Habito.objects.filter(usuario=self.request.user)
    
# Exclui os hábitos.
class HabitoDeleteView(LoginRequiredMixin, DeleteView):
    model = Habito
    template_name = 'habitos/habito_confirm_delete.html'
    success_url = reverse_lazy('listar-habito')

    def get_queryset(self):
        return Habito.objects.filter(usuario=self.request.user)
    
