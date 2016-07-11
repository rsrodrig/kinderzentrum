"""module for testing"""
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

class MySeleniumTests(StaticLiveServerTestCase):
    """Class for testing registering a patien"""

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        user = User.objects.create_user("gabriel", password="gabriel")
        user.groups.add(1)
        cls.selenium = webdriver.Firefox(capabilities=firefox_capabilities)
        #cls.selenium = WebDriver()
        cls.client = Client()
        cls.client.login(username="gabriel", password='gabriel') #Native django test client
        cookie = cls.client.cookies['sessionid']
        #selenium will set cookie domain based on current page domain
        cls.selenium.get(cls.live_server_url + '/admin/')
        cls.selenium.add_cookie({'name': 'sessionid', 'value': cookie.value,
                                 'secure': False, 'path': '/'})
        cls.selenium.refresh() #need to update page for logged in user
        cls.selenium.get(cls.live_server_url + '/admin/')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def waitForPageLoad(self, timeout=5):
        """Waits for a page load"""
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body')
        )

    def test_login(self):
        """tests login"""
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('gabriel')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('gabriel')
        self.selenium.find_element_by_id("loginBtn").click()
        self.waitForPageLoad()
        title = self.selenium.find_element_by_tag_name('title')
        print "Title", title


    def test_registro_paciente(self):
        """Fills paciente form"""
        #self.test_login()
        self.selenium.get('%s%s' % (self.live_server_url, '/registro'))
        print "Title", self.selenium.title
        self.fill_paciente_form()
        self.selenium.find_element_by_css_selector("#nav2 > a").click()
        self.fill_familiar_form()
        #self.selenium.find_element_by_css_selector("#nav3 > a").click()
        self.fill_medico_form()
        #self.selenium.find_element_by_id("nav4").click()
        self.selenium.find_element_by_css_selector("#nav4 > a").click()
        self.fillDescripcion()
        #self.selenium.find_element_by_css_selector("#nav5 > a").click()
        self.fill_historial_madre_form()
        self.selenium.find_element_by_css_selector("#nav6 > a").click()
        self.fill_gestacion_form()
        self.selenium.find_element_by_css_selector("#nav7 > a").click()
        self.fill_nacimiento_form()
        self.selenium.find_element_by_css_selector("#nav8 > a").click()
        self.fill_recien_nacido_form()
        self.selenium.find_element_by_css_selector("#nav9 > a").click()
        self.fill_primeros_dias_form()
        self.selenium.find_element_by_css_selector("#nav10 > a").click()
        self.fill_alimentacion_form()
        self.selenium.find_element_by_css_selector("#nav11 > a").click()
        self.fill_datos_familiares_form()
        self.selenium.find_element_by_id("enviar").click()
        self.waitForPageLoad()
        print "Title", self.selenium.title

    def fill_paciente_form(self):
        """fills first form:paciente info"""
        nombre = self.selenium.find_element_by_id("id_paciente-nombres")
        nombre.send_keys("nombre")
        apellido = self.selenium.find_element_by_id("id_paciente-apellidos")
        apellido.send_keys("apellidos")
        self.selenium.find_element_by_id("id_paciente-sexo_0").click()
        self.selenium.find_element_by_id("id_paciente-lugar_nacimiento").send_keys("lugar")
        self.selenium.find_element_by_id("id_paciente-fecha_nacimiento").send_keys("10/1'/2010")
        self.selenium.find_element_by_id("id_paciente-nacionalidad").send_keys("ecuador")


    def fill_familiar_form(self):
        """Fill familiar form"""
        field = self.selenium.find_element_by_id
        field("id_familiares-0-parentesco").send_keys("madre")
        field("id_familiares-0-nombres").send_keys("madre")
        field("id_familiares-0-apellidos").send_keys("madre")
        Select(field("id_familiares-0-nivel_estudio")).select_by_index(2)
        field("id_familiares-0-direccion").send_keys("madre")
        field("id_familiares-0-telefonos").send_keys("madre")
        field("id_familiares-0-empresa").send_keys("madre")
        field("id_familiares-0-direccion_empresa").send_keys("madre")
        Select(field("id_familiares-0-jornada")).select_by_index(2)
        
    def fill_medico_form(self):
        """Fill medico form"""
        field = self.selenium.find_element_by_id
        field("id_medico-0-nombres").send_keys("madre")
        field("id_medico-0-apellidos").send_keys("madre")
        field("id_medico-0-direccion").send_keys("madre")
        field("id_medico-0-telefonos").send_keys("madre")
        field("id_medico-0-area").send_keys("madre")

    def fillDescripcion(self):
        """Fill descripcion paciente form"""
        field = self.selenium.find_element_by_id
        field("id_descripcion_paciente-preocupacion").send_keys("Preocupacion")
        field("id_descripcion_paciente-edad_disc_molestia").send_keys("12")
        field("id_descripcion_paciente-tratamiento_1").click()
        field("id_descripcion_paciente-tipo_terapia_2").click()
        select = Select(field('id_descripcion_paciente-limitaciones_movimiento'))
        select.select_by_index(2)
        select = Select(field('id_descripcion_paciente-had_convulsion'))
        select.select_by_index(2)

    def fill_historial_madre_form(self):
        """Fill historial madre form"""
        field = self.selenium.find_element_by_id
        field("id_historial_madre-tuvo_defuncion_fetal_1").click()
        field("id_historial_madre-uso_anticonceptivo_1").click()
        field("id_historial_madre-hijos_nacidos_vivos").send_keys("1")
        field("id_historial_madre-tuvo_hijos_muertos_1").click()
        field("id_historial_madre-embarazos").send_keys("2")
        
    def fill_gestacion_form(self):
        """Fill gestacion form"""
        field = self.selenium.find_element_by_id
        field("id_gestacion-num_embarazo").send_keys(3)
        field("id_gestacion-curso_prenatal_1").click()
        field("id_gestacion-vacuna_tetano_0").click()
        field("id_gestacion-comunicacion_bebe_2").click()
        select = Select(field("id_situacion-0-periodo"))
        select.select_by_index(2)
        Select(field("id_actividad-3-periodo")).select_by_index(2)

    def fill_nacimiento_form(self):
        """Fill nacimiento form"""
        field = self.selenium.find_element_by_id
        field("id_nacimiento-tipo_lugar_nacimiento_1").click()
        field("id_nacimiento-nombre_lugar_nacimiento").send_keys("nombre")
        field("id_nacimiento-semana_gestacion").send_keys(25)
        field("id_nacimiento-metodo_nacimiento_1").click()
        field("id_nacimiento-manera_inicio_parto_0").click()
        field("id_nacimiento-tipo_ruptura_fuente_1").click()
        field("id_nacimiento-sentimientos_parto").send_keys("sentimientos20")
        field("id_nacimiento-sentimientos_nacimiento").send_keys("senti20")
        field("id_nacimiento-duracion_nacimiento").send_keys("20")
        field("id_nacimiento-gemelar_1").click()
        field("id_nacimiento-primera_parte_cuerpo_1").click()
        field("id_nacimiento-complicaciones_1").click()
        field("id_nacimiento-medicamentos_parto_1").click()
        field("id_nacimiento-complicaciones_cordon_1").click()
        
    def fill_recien_nacido_form(self):
        """Fill recien nacido form"""
        field = self.selenium.find_element_by_id
        field("id_recien_nacido-edad_madre").send_keys("29")
        field("id_recien_nacido-edad_padre").send_keys("29")
        field("id_recien_nacido-peso").send_keys("29")
        field("id_recien_nacido-tamanio").send_keys("29")
        field("id_recien_nacido-diametro_encefalico").send_keys("29")
        field("id_recien_nacido-apgar_score_0").click()
        field("id_recien_nacido-complicaciones_nacimiento_4").click()
        field("id_recien_nacido-hubo_apego_precoz_1").click()
        field("id_recien_nacido-tiempo_sostener_bebe_1").click()
        field("id_recien_nacido-permanecio_internado_1").click()
        field("id_recien_nacido-primera_lactancia_0").click()

    def fill_primeros_dias_form(self):
        """Fill primeros dias form"""
        field = self.selenium.find_element_by_id
        field("id_primeros_dias-clinica_1").click()
        field("id_primeros_dias-situaciones_despues_nacimiento_1").click()
        field("id_primeros_dias-icteria_1").click()
        field("id_primeros_dias-examenes_1").click()
        field("id_primeros_dias-dormia_toda_noche_0").click()
        field("id_primeros_dias-lugar_dormir_0").click()
        field("id_primeros_dias-descripcion_bebe").send_keys("Descripcion")
        field("id_primeros_dias-descripcion_madre").send_keys("Descripcion")

    def fill_alimentacion_form(self):
        """Fill alimentacion form"""
        field = self.selenium.find_element_by_id
        field("id_alimentacion-lactancia_1").click()
        field("id_alimentacion-afecciones_0").click()
        field("id_alimentacion-enfermedades_0").click()
        field("id_alimentacion-edad_alimentacion_complementaria").send_keys("1")
        field("id_alimentacion-forma_alimento_0").click()
        field("id_alimentacion-lugar_desayuno").send_keys("1")
        field("id_alimentacion-lugar_comida_media_manana").send_keys("1")
        field("id_alimentacion-lugar_almuerzo").send_keys("1")
        field("id_alimentacion-lugar_comida_media_tarde").send_keys("1")
        field("id_alimentacion-lugar_cena").send_keys("1")
        field("id_alimentacion-lugar_comida_otro").send_keys("1")
        field("id_alimentacion-alimento_preferido").send_keys("1")
        field("id_alimentacion-alimento_rechazado").send_keys("1")
        field("id_alimentacion-suplementos_1").click()
        field("id_alimentacion-apetito_0").click()
        field("id_alimentacion-difiere_alimentacion_1").click()


    def fill_datos_familiares_form(self):
        """Fill datos familiares form"""
        field = self.selenium.find_element_by_id
        field("id_familiares_otros-numero_hermanos").send_keys("0")
        field("id_familiares_otros-tipo_enfermedad_parientes").send_keys("0")
        field("id_familiares_otros-orientacion_a_institucion_0").click()
class MyTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(MyTestCase, cls).setUpClass()
        cls.client = Client()
        user = User.objects.create_user("gabriel", password="gabriel")
        user.groups.add(1)
        cls.client.login(username='gabriel', password='gabriel')

    @classmethod
    def tearDownClass(cls):
        super(MyTestCase, cls).tearDownClass()
         

    def test_registro(self):
        self.client.login(username='gabriel', password='gabriel')
        response = self.client.post('/registro', follow=True)
        print response.content, response.status_code
        #print "response", response, response.status_code
    

