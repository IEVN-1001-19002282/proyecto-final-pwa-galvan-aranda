import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RestService } from 'src/app/service/rest.service';

@Component({
  selector: 'app-menubar',
  templateUrl: './menubar.component.html',
  styleUrls: ['./menubar.component.css']
})
export class MenubarComponent implements OnInit {

  constructor(private rest: RestService, private route: Router) { }



  usuarioo = {
    id_usuario: 0,
    nombre_usuario: "",
    correo_usuario:"",
    contrasena_usuario: "",
    tipo_usuario: 0
  }

  validar=0;
  


  ngOnInit(): void {
    var datos = sessionStorage.getItem('datos_usuario')
    if (datos){
      this.usuarioo = JSON.parse(datos)
      this.validar = 1;
    }else{
      this.validar = 0;
      // this.usuarioo.id_usuario = 0;
      // this.usuarioo.nombre_usuario = "";
      // this.usuarioo.correo_usuario = "";
      // this.usuarioo.contrasena_usuario ="";
      // this.usuarioo.tipo_usuario = 0;
      return
    }
    
    
  }

  async cerrarSesion(){
    var datos = sessionStorage.getItem('datos_usuario')
    if (datos){
      var usuario = JSON.parse(datos)
      var res = await this.rest.PostRequest('cerrar_sesion', usuario).toPromise();
      if (res.exito){
        sessionStorage.removeItem('datos_usuario')
        this.route.navigate(['login'])
      }
      // else{
      //   this.route.navigate(['login'])
      // }
    }else{
      this.route.navigate(['login'])
    }
    
  }

}
