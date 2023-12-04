import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RestService } from 'src/app/service/rest.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {


  discos = [{
    id_producto: 0,
    imagen_producto: "",
    nombre_producto: "",
    descripcion_producto: "",
    artista_producto: "",
    ano_producto: 0,
    precio_producto: 0.0,
    stock_producto: 0,
    estatus_producto:0
  }
  ]

  constructor(private rest: RestService, private route: Router) { }

  ngOnInit(): void {
    var datos = sessionStorage.getItem('datos_usuario')
    if (datos){
      var usuario = JSON.parse(datos)
      
      if (usuario.tipo_usuario!=2){
        this.route.navigate(["discos"])
      }
    }else{
      this.route.navigate(["login"])
      return
    }
    this.getLibros()
  }


  async getLibros() {
    var res = await this.rest.GetRequest('home').toPromise();
    this.discos = res.productos;
    console.log(this.discos)
  }

  
}
