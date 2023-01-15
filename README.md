## Django API Rest
La aplicación consiste en un sistema de reservas para un hotel, donde los usuarios pueden ver las habitaciones disponibles, hacer reservas, ver y actualizar sus reservas existentes, y procesar pagos. Los endpoints incluyen la creación y listado de habitaciones, reservas, detalles y actualizaciones de reservas, y procesamiento de pagos. El sistema tambien esta dockerizado para facilitar su implementacion en entornos de produccion.

# Endpoints
* `api/create-room/`: Crear nuevas habitaciones en el hotel para facilitar el guardado de la información en la base de datos.

* `api/rooms/`: Obtener todas las habitaciones disponibles en el hotel para poder realizar reservas.

* `api/reserve/`: Reservar una habitación en el hotel en una fecha específica, recibiendo información como el id de la habitación, fechas de inicio y fin, nombre y correo electrónico del cliente. Crea una nueva reserva y confirma al cliente.

* `api/reservations/`: Este endpoint retorna una lista con la informacion de las reservas hechas hasta el momento.

* `api/reservations/<int:pk>/`: Obtener información detallada de una reserva específica para llevar un registro de las reservas.

* `api/reservations/<int:pk>/update/`: Actualizar la información de una reserva específica para adaptarse a los cambios y asegurar la satisfacción del cliente.

* `api/reservations/<int:pk>/cancel/`: Permite cancelar una reserva específica mediante su id.

* `api/payment/`: Enviar los datos de tarjeta de crédito y generar un token de pago para procesar el pago en el siguiente endpoint.

* `api/payment/<int:pk>/charge/`: Cargar el monto de la reserva a la tarjeta del cliente y cambiar el estado de la reserva en caso de éxito. Recibe la id de la reserva y el token de pago.

## Sistema de pagos

Para configurar el sistema de pagos, es necesario obtener una cuenta en Stripe (https://stripe.com/) y obtener las llaves de publicación y privadas. Estas llaves deben ser agregadas en el archivo con sus variables de entorno.
