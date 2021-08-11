


clientes = [
    
]

def convert_to_json(tupla):
   claves= ['id','nombre', 'telefono','direccion','num_documento','email']
   return dict(zip(claves,tupla))



productos = [
    
]

def convert_to_json_products(tupla2):
   valores = ['id_producto','codigo_producto','nombre_producto','precio_producto','marca_producto', 'stock_producto', 'descripcion']
   return dict(zip(valores,tupla2))