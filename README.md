## Django API Rest
La aplicación consiste en un sistema de reservas para un hotel, donde los usuarios pueden ver las habitaciones disponibles, hacer reservas, ver y actualizar sus reservas existentes, y procesar pagos. Los endpoints incluyen la creación y listado de habitaciones, reservas, detalles y actualizaciones de reservas, y procesamiento de pagos. El sistema tambien esta dockerizado para facilitar su implementacion en entornos de produccion.

# Endpoints

`api/create-room/`: Este endpoint permite crear nuevas habitaciones en el hotel. Es necesario tener esta funcionalidad para facilitar guardar la información de las habitaciones en la base de datos.

`api/rooms/`: Este endpoint permite obtener todas las habitaciones disponibles en el hotel. Es importante tener acceso a esta información para poder realizar reservas.

`api/reserve/`: Este endpoint permite reservar una habitación en el hotel en una fecha específica. Recibe una serie de parámetros como el id de la habitación, las fechas de inicio y fin de la reserva, el nombre y correo electrónico del cliente, entre otros. Con esta información, se crea una nueva reserva en la base de datos y se confirma al cliente.

`api/reservations/<int:pk>/`: Este endpoint permite obtener información detallada de una reserva específica. Es importante tener acceso a esta información para poder llevar un registro de las reservas realizadas.

`api/reservations/<int:pk>/update/`: Este endpoint permite actualizar la información de una reserva específica. Es importante tener esta funcionalidad para poder adaptarse a los cambios en las reservas y asegurar la satisfacción del cliente.

`api/payment/`: Este endpoint permite enviar los datos de tarjeta de credito y genera un token de pago para luego poder procesar el pago con el siguiente endpoint.

`payment/<int:pk>/charge/`: Este endpoint se encarga de cargar el monto de la reserva a la tarjeta del cliente y de ser exitoso cambia el estado de la reserva. Recibe la id de la reserva y el token de pago.
