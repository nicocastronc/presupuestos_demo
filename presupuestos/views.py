from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Servicio, Presupuesto, ItemPresupuesto
from .forms import ClienteForm, ServicioForm, ServicioForm, ItemPresupuestoForm, PresupuestoForm
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import tempfile

def home(request):
    return render(request, 'home.html')

#CLIENTES
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()

    #Lógica para poder filtrar las consultas.
    query = request.GET.get('q')
    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query)
        )

    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes, 'query': query})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_cliente.html', {'form': form})

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_cliente.html', {'form': form})

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})

#SERVICIOS

@login_required
def servicio_lista(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios/lista.html', {'servicios': servicios})

@login_required
def servicio_crear(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicio_lista')
    else:
        form = ServicioForm()
    return render(request, 'servicios/form.html', {'form': form})

@login_required
def servicio_editar(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('servicio_lista')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'servicios/form.html', {'form': form})

@login_required
def servicio_eliminar(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        return redirect('servicio_lista')
    return render(request, 'servicios/confirmar_eliminar.html', {'servicio': servicio})


#PRESUPUESTOS
def get_item_form(request):
    # Obtener todos los servicios disponibles
    servicios = Servicio.objects.all()

    # Renderizar un template parcial para el formulario de ítem
    return render(request, 'presupuestos/items_form.html', {
        'servicios': servicios
    })

@login_required
def crear_presupuesto(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.freelancer = request.user
            presupuesto.save()

            # Procesar ítems del presupuesto
            servicios = request.POST.getlist('servicio')
            precios = request.POST.getlist('precio')

            for servicio_id, precio in zip(servicios, precios):
                servicio = Servicio.objects.get(id=servicio_id)
                ItemPresupuesto.objects.create(
                    presupuesto=presupuesto,
                    servicio=servicio,
                    cantidad=1,  # Fijo en 1 si no aplica
                    precio_total=float(precio)
                )

            return redirect('detalle_presupuesto', pk=presupuesto.pk)
    else:
        form = PresupuestoForm()

    servicios = Servicio.objects.all()
    return render(request, 'presupuestos/crear.html', {
        'form': form,
        'servicios': servicios
    })

@login_required
def detalle_presupuesto(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    return render(request, 'presupuestos/detalle.html', {'presupuesto': presupuesto})

@login_required
def generar_pdf(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)

    # Renderizar el template HTML
    html_string = render_to_string('presupuestos/pdf_template.html', {
        'presupuesto': presupuesto,
    })

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=True) as output:
        # Convertir HTML a PDF
        HTML(string=html_string).write_pdf(output.name)

        # Leer el archivo PDF
        with open(output.name, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'filename="presupuesto_{presupuesto.id}.pdf"'
            return response