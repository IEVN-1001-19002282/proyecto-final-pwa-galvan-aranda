import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RestService } from 'src/app/service/rest.service';

@Component({
  selector: 'app-crear-libro',
  templateUrl: './crear-libro.component.html',
  styleUrls: ['./crear-libro.component.css']
})
export class CrearLibroComponent implements OnInit {

  no_disponible = "https://dynamicmediainstitute.org/wp-content/themes/dynamic-media-institute/imagery/default-book.png";
  imagen: any = null;

  libro = {
    id_producto: 0,
    imagen_producto: null,
    nombre_producto: "",
    descripcion_producto: "",
    artista_producto: "",
    ano_producto: 0,
    precio_producto: 0.0,
    stock_producto: 0,
    estatus_producto:0
  };

  messageOk = null;
  messageErr = null;

  constructor(private rest: RestService, private route: Router) { }

  ngOnInit(): void {
    var datos = sessionStorage.getItem('datos_usuario')
    if (datos){
      var usuario = JSON.parse(datos)
      
      if (usuario.tipo_usuario!=1){
        this.route.navigate([""])
      }
    }else{
      this.route.navigate(["login"])
      return
    }
  }

  uploadImagen(event: any) {
    if (event.target.files && event.target.files[0]) {
      var file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = e => this.imagen = reader.result;
      reader.readAsDataURL(file);
    }
  }

  async agregar() {
    // obtener imagen
    this.libro.imagen_producto = this.imagen;
    // mostrar datos
    console.log(this.libro.id_producto)
    console.log(this.libro.imagen_producto)
    console.log(this.libro.nombre_producto)
    console.log(this.libro.descripcion_producto)
    console.log(this.libro.artista_producto)
    console.log(this.libro.ano_producto)
    console.log(this.libro.precio_producto)
    console.log(this.libro.stock_producto)
    console.log(this.libro.estatus_producto)

    try {
      // peticion
      // podemos utilizar await o no
      var res = await this.rest.PostRequest("registrar_producto", this.libro).toPromise();
      console.log(res);
      // resetear datos
      this.libro.id_producto = 0;
      this.libro.imagen_producto = null;
      this.libro.nombre_producto = "";
      this.libro.descripcion_producto = "";
      this.libro.artista_producto = "";
      this.libro.ano_producto = 0;
      this.libro.precio_producto = 0.0;
      this.libro.stock_producto = 0;
      this.libro.estatus_producto = 0;
      this.messageOk = res.message;

    } catch(error: any) {
      this.messageErr = error.error.message
    }
  }

  cancelar() {
    this.route.navigate(["discos"])
  }

  cerrarAlert1() {
    this.messageOk = null;
  }

  cerrarAlert2() {
    this.messageErr = null;
  }
}
