import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RestService } from 'src/app/service/rest.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {


  usuario = {
    id_usuario: 0,
    nombre_usuario: "",
    correo_usuario:"",
    contrasena_usuario: "",
    tipo_usuario: 0
  }
  constructor(private rest: RestService, private route: Router) { }

  ngOnInit(): void {
    var datos = sessionStorage.getItem('datos_usuario')
    if (datos){
      var usuario = JSON.parse(datos)
      
      if (usuario.tipo_usuario==1){
        this.route.navigate(["discos"])
      }else{
        this.route.navigate([""])
      }
    }else{
//      this.route.navigate(["register"])
      return
    }
  }

  async registrarUsuario(){
      var res = await this.rest.PostRequest('registrar_usuario', this.usuario).toPromise()
      
      console.log(res);
      //reiniciar datos
      // this.usuario.id_usuario = 0;
      // this.usuario.nombre_usuario = "";
      // this.usuario.correo_usuario = "";
      // this.usuario.contrasena_usuario = "";
      // this.usuario.tipo_usuario = 0;
    
    

  }


}
