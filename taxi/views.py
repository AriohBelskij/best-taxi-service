from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from sweetify.views import SweetifySuccessMixin
from django.template.loader import render_to_string

from .models import Driver, Car, Manufacturer, CarComments
from .forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
    CarCommentForm,
    DriverSettingsForm,
)


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    queryset = Manufacturer.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ManufacturerListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ManufacturerSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = ManufacturerSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer


@method_decorator(staff_member_required(login_url="/"), name="dispatch")
class ManufacturerCreateView(
    LoginRequiredMixin, SweetifySuccessMixin, generic.CreateView
):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Done! manufacturer created!"


@method_decorator(staff_member_required(login_url="/"), name="dispatch")
class ManufacturerUpdateView(
    LoginRequiredMixin, SweetifySuccessMixin, generic.UpdateView
):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Manufacturer successfully update"


@method_decorator(staff_member_required(login_url="/"), name="dispatch")
class ManufacturerDeleteView(SweetifySuccessMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Done!"


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 4
    queryset = Car.objects.select_related("manufacturer",)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("model", "")
        context["search_form"] = CarSearchForm(initial={"model": model})

        return context

    def get_queryset(self):
        form = CarSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                model__icontains=form.cleaned_data["model"]
            )
        return self.queryset


class CarDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Car
    form_class = CarCommentForm
    queryset = Car.objects.prefetch_related(
        "comments_car__likes__car_comment", "comments_car__driver__cars"
    )

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "taxi:car-detail", kwargs={"pk": self.get_object().id}
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.car = self.get_object()
        self.object.driver = self.request.user
        self.object.save()
        return super().form_valid(form)


@method_decorator(staff_member_required(login_url="/"), name="dispatch")
class CarCreateView(
    LoginRequiredMixin, SweetifySuccessMixin, generic.CreateView
):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Done!"


@method_decorator(staff_member_required(login_url="/"), name="dispatch")
class CarUpdateView(SweetifySuccessMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Done!"


@method_decorator(staff_member_required(login_url="/"), name="dispatch")
class CarDeleteView(SweetifySuccessMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Done!"


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 4
    queryset = Driver.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriverListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = DriverSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = DriverSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = Driver.objects.prefetch_related("cars__manufacturer",)


@method_decorator(staff_member_required(login_url="/"), name="dispatch")
class DriverCreateView(SweetifySuccessMixin, generic.CreateView):
    model = get_user_model()
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")
    success_message = "Driver successfully create"

class DriverLicenseUpdateView(
    LoginRequiredMixin, SweetifySuccessMixin, generic.UpdateView
):
    model = get_user_model()
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")
    success_message = "License successfully update"

    def get(self, request, *args, **kwargs):
        driver = self.get_object()
        if not request.user.is_staff:
            if request.user.id == driver.id:
                return super(DriverLicenseUpdateView, self).get(
                    request, *args, **kwargs
                )
        if request.user.is_staff:
            return super(DriverLicenseUpdateView, self).get(
                request, *args, **kwargs
            )
        return HttpResponseRedirect("/")

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "taxi:driver-detail", kwargs={"pk": self.get_object().id}
        )

    
class DriverDeleteView(
    LoginRequiredMixin, SweetifySuccessMixin, generic.DeleteView
):
    model = get_user_model()
    success_url = reverse_lazy("taxi:driver-list")
    permission_required = "taxi.delete-driver"
    success_message = "User deleted successfully"
    
    def get(self, request, *args, **kwargs):
        profile = self.get_object().driver.id
        if not request.user.is_staff:
            if request.user.id == profile:
                return super(DriverDeleteView, self).get(
                    request, *args, **kwargs
                )
        if request.user.is_staff:
            return super(DriverDeleteView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect("/")    


@login_required
def toggle_assign_to_car(request, pk):
    driver = Driver.objects.get(id=request.user.id)
    if Car.objects.get(id=pk) in driver.cars.all():
        driver.cars.remove(pk)
    else:
        driver.cars.add(pk)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))


class RegistrationView(generic.CreateView):
    model = get_user_model()
    form_class = DriverCreationForm
    template_name = "taxi/registration.html"
    success_url = reverse_lazy("taxi:registration-complete")


def registration_complete(request):
    return render(request, "registration/register.html")


class CommentDeleteView(SweetifySuccessMixin, generic.DeleteView):
    model = CarComments
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Comment successfully deleted"

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "taxi:car-detail", kwargs={"pk": self.get_object().car.id}
        )

    def get(self, request, *args, **kwargs):
        comment = self.get_object().driver.id
        if not request.user.is_staff:
            if request.user.id == comment:
                return super(CommentDeleteView, self).get(
                    request, *args, **kwargs
                )
        if request.user.is_staff:
            return super(CommentDeleteView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect("/")


class DriverSettingsView(
    LoginRequiredMixin, SweetifySuccessMixin, generic.UpdateView
):
    model = get_user_model()
    form_class = DriverSettingsForm
    success_url = reverse_lazy("taxi:driver-list")
    success_message = "Settings updated"

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "taxi:driver-detail", kwargs={"pk": self.get_object().id}
        )

    def get(self, request, *args, **kwargs):
        driver = self.get_object()
        if not request.user.is_staff:
            if request.user.id == driver.id:
                return super(DriverSettingsView, self).get(
                    request, *args, **kwargs
                )
        if request.user.is_staff:
            return super(DriverSettingsView, self).get(
                request, *args, **kwargs
            )
        return HttpResponseRedirect("/")


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


@login_required
def like_and_unlike(request, *args, **kwargs):
    comment = get_object_or_404(
        CarComments,
        id=request.POST.get("key"),  # take key from js script in base.html
    )

    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        comment.save()
    else:
        comment.likes.add(request.user)
        comment.save()
    context = {"comment": comment}
    if is_ajax(request):
        print(context)
        html = render_to_string(
            "taxi/like-section.html", context=context, request=request
        )
        return JsonResponse({"form": html})
    return HttpResponseRedirect(
        reverse_lazy("taxi: car-detail"), args=[kwargs["pk"]]
    )
