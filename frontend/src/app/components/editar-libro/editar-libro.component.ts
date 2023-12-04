import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RestService } from 'src/app/service/rest.service';

@Component({
  selector: 'app-editar-libro',
  templateUrl: './editar-libro.component.html',
  styleUrls: ['./editar-libro.component.css']
})
export class EditarLibroComponent implements OnInit {

  no_disponible = "https://dynamicmediainstitute.org/wp-content/themes/dynamic-media-institute/imagery/default-book.png";
  imagen: any = null;

  libro = {
    id_producto: 0,
    imagen_producto: "",
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
    this.cargarLibro();
  }

  async cargarLibro() {
    var id = sessionStorage.getItem('id');
    console.log(id)
    var res = await this.rest.GetRequest('listarDiscos/' + id).toPromise();
    console.log(res)
    
    
    this.libro.id_producto = res.producto.id_producto;
    this.libro.imagen_producto = res.producto.imagen_producto;
    this.libro.nombre_producto = res.producto.nombre_producto;
    this.libro.descripcion_producto = res.producto.descripcion_producto;
    this.libro.artista_producto = res.producto.artista_producto;
    this.libro.ano_producto = res.producto.ano_producto;
    this.libro.precio_producto = res.producto.precio_producto;
    this.libro.stock_producto = res.producto.stock_producto;
    this.libro.estatus_producto = res.producto.estatus_producto;
    this.imagen = this.libro.imagen_producto;
  }

  uploadImagen(event: any) {
    if (event.target.files && event.target.files[0]) {
      var file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = e => this.imagen = reader.result;
      reader.readAsDataURL(file);
    }
  }

  async actualizar() {
    // obtener imagen
    this.libro.imagen_producto = this.imagen;

    var id = sessionStorage.getItem('id');

    try {
      var res = await this.rest.PostRequest('editarProducto', this.libro).toPromise();
      this.messageOk = res.message;
      if (res.exito){
        this.route.navigate(["discos"])
      }else{
        console.log("Error")
      }
    } catch (error: any) {
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
