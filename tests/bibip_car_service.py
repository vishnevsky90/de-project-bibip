from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from datetime import datetime
from decimal import Decimal


class CarService:
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir

        open(self.tmpdir + '/models_index.txt', 'a').close()
        open(self.tmpdir + '/models.txt', 'a').close()
        open(self.tmpdir + '/cars.txt', 'a').close()
        open(self.tmpdir + '/cars_index.txt', 'a').close()
        open(self.tmpdir + '/sales_index.txt', 'a').close()
        open(self.tmpdir + '/sales.txt', 'a').close()

    # Задание 1. Сохранение автомобилей и моделей

    def add_model(self, model: Model) -> Model:
        with open(self.tmpdir+'/models.txt', 'a+') as m:
            str_m = (
                ", ".join([str(model.id), model.model_name, model.brand]) + '\n')
            m.write(str_m)

        count_lines = 1
        try:
            with open(self.tmpdir+'/models_index.txt', 'r') as mi:
                lines = mi.readlines()
                count_lines = len(lines)+1
        except FileNotFoundError:
            pass

        with open(self.tmpdir+'/models_index.txt', 'a+') as mi:
            str_mi = (", ".join([str(count_lines), str(model.id)]) + '\n')
            mi.write(str_mi)
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        with open(self.tmpdir+'/cars.txt', 'a+') as c:
            str_c = (", ".join([car.vin, str(car.model), str(
                car.price), str(car.date_start), car.status]) + '\n')
            c.write(str_c)
        count_lines = 1
        try:
            with open(self.tmpdir+'/cars_index.txt', 'r') as ci:
                lines = ci.readlines()
                count_lines = len(lines)+1
        except FileNotFoundError:
            pass

        with open(self.tmpdir+'/cars_index.txt', 'a+') as ci:
            str_ci = (", ".join([str(count_lines), car.vin]) + '\n')
            ci.write(str_ci)
        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        with open(self.tmpdir+'/sales.txt', 'a+') as s:
            str_s = (", ".join([sale.sales_number, sale.car_vin, str(
                sale.cost), str(sale.sales_date)]) + '\n')
            s.write(str_s)

        count_lines = 1
        try:
            with open(self.tmpdir+'/sales_index.txt', 'r') as si:
                lines = si.readlines()
                count_lines = len(lines)+1
        except FileNotFoundError:
            pass

        with open(self.tmpdir+'/sales_index.txt', 'a+') as si:
            str_si = (", ".join([str(count_lines), sale.car_vin]) + '\n')
            si.write(str_si)
        car_index = None

        with open(self.tmpdir+'/cars_index.txt', 'r') as ci:
            index_lines = ci.readlines()
            # Поиск VIN в index
            for index, line in enumerate(index_lines):
                # разбиваем строку на части по запятой и пробелу, возвращая список элементов.
                list = line.strip().split(', ')
                vin = list[1]  # Получаем второй элемент из списка
                if vin == sale.car_vin:
                    car_index = int(list[0])  # Присваиваем индекс
                    break  # Завершаем цикл, если нашли VIN
        if car_index is not None:
            with open(self.tmpdir+'/cars.txt', 'r') as ci:
                lines_car = ci.readlines()

            # Изменяем статус автомобиля на 'sold'
            lines_car[car_index - 1] = lines_car[car_index - 1].replace(lines_car[car_index - 1].strip().split(', ')[-1], 'sold')
            parts = lines_car[car_index - 1].strip().split(', ')
            # Записываем изменения обратно в файл
            with open(self.tmpdir+'/cars.txt', 'w') as file_4:
                file_4.writelines(lines_car)
            # Создание объекта Car, который мы вернем
            car = Car(vin=parts[0],
                      model=int(parts[1]),
                      price=Decimal(parts[2]),
                      date_start=datetime.strptime(
                          parts[3], '%Y-%m-%d %H:%M:%S'),
                      status=CarStatus('sold')
                      )
            return car  # Возвращаем объект Car
        return None

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        list = []
        with open(self.tmpdir+'/cars.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(', ')  # Разделяем строку на части
                if parts[-1] == status:
                    car = Car(
                        vin=parts[0],
                        model=int(parts[1]),
                        price=Decimal(parts[2]),
                        date_start=datetime.strptime(
                            parts[3], '%Y-%m-%d %H:%M:%S'),
                        status=CarStatus(parts[-1])
                    )
                    list.append(car)
        # Сортировка списка автомобилей по VIN
        list = sorted(list, key=lambda car: car.vin)
        return list

    # Задание 4. Детальная информация
    def get_car_info(self, car_vin: str) -> CarFullInfo | None:
        car_index = None

        with open(self.tmpdir+'/cars_index.txt', 'r') as file_3:
            index_lines = file_3.readlines()

            model_index = None
            sales_index = None
            model = None
            sales = None
            model_name = ''
            model_brand = ''
            price = Decimal('0.0')
            date_start = '1970-01-01 00:00:00'
            status = CarStatus('available')
            sales_date = None
            sales_cost = None
            for index, line in enumerate(index_lines):
                # разбиваем строку на части по запятой и пробелу, возвращая список элементов.
                list = line.strip().split(', ')
                vin = list[1]  # Получаем второй элемент из списка
                if vin == car_vin:
                    car_index = int(list[0])  # Присваиваем индекс
                    break  # Завершаем цикл, если нашли VIN

            if car_index is not None:
                with open(self.tmpdir+'/cars.txt', 'r') as file_4:
                    lines_car = file_4.readlines()

                car = lines_car[car_index - 1]
                parts = car.strip().split(', ')
                model = parts[1]
                price = Decimal(parts[2])
                date_start = parts[3]
                status = CarStatus(parts[4])

                with open(self.tmpdir+'/models_index.txt', 'r') as file_model_index:
                    lines = file_model_index.readlines()

                    for i, line in enumerate(lines):
                        mi = line.strip().split(', ')
                        model_list = mi[1]
                        if model_list == model:
                            model_index = int(mi[0])
                            break
                    if model_index is not None:
                        with open(self.tmpdir+'/models.txt', 'r') as file_model:
                            lines = file_model.readlines()

                        model = lines[model_index - 1]
                        parts = model.strip().split(', ')
                        model_name = parts[1]
                        model_brand = parts[2]

                with open(self.tmpdir+'/sales_index.txt', 'r+') as file_sales_index:
                    lines = file_sales_index.readlines()

                    for i, line in enumerate(lines):
                        si = line.strip().split(', ')
                        sales_list = si[1]
                        if sales_list == car_vin:
                            sales_index = int(si[0])
                            break
                    if sales_index is not None:
                        with open(self.tmpdir+'/sales.txt', 'r+') as file_sales:
                            lines = file_sales.readlines()
                        sales = lines[sales_index-1]
                        parts = sales.strip().split(', ')
                        if status == CarStatus.sold:
                            sales_cost = parts[2]
                            sales_date = parts[3]
                        else:
                            sales_cost = None
                            sales_date = None
        new = None
        if car_index:
            new = CarFullInfo(
                vin=car_vin,
                model_name=model_name,
                model_brand=model_brand,
                price=Decimal(price),
                date_start=datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S'),
                status=status,
                sales_date=datetime.strptime(
                    sales_date, '%Y-%m-%d %H:%M:%S') if sales_date else None,
                sales_cost=Decimal(sales_cost) if sales_cost else None
            )
        return new

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:

        car_index = None

        with open(self.tmpdir+'/cars_index.txt', 'r') as file_car_index:
            index_lines = file_car_index.readlines()
            # Поиск VIN в index
            for index, line in enumerate(index_lines):
                # разбиваем строку на части по запятой и пробелу, возвращая список элементов.
                list = line.strip().split(', ')
                car_vin = list[1]  # Получаем второй элемент из списка
                if car_vin == vin:
                    car_index = int(list[0])  # Присваиваем индекс
                    break  # Завершаем цикл, если нашли VIN
        if car_index is not None:
            del index_lines[car_index - 1]
            with open(self.tmpdir+'/cars_index.txt', 'w') as file_car_index:
                file_car_index.writelines(index_lines)

            with open(self.tmpdir+'/cars.txt', 'r') as file_car:
                lines_car = file_car.readlines()
                car = lines_car[car_index - 1]
                parts = car.strip().split(', ')
                model = parts[1]
                price = parts[2]
                date_start = parts[3]
                status = CarStatus(parts[4])
            # Удаляем нужную строку
            del lines_car[car_index - 1]
            # Записываем изменения обратно в файл
            with open(self.tmpdir+'/cars.txt', 'w') as file_car:
                file_car.writelines(lines_car)
                # записываем новую строку с новым vin
                file_car.write(", ".join([new_vin, str(model), str(price),
                                          str(date_start), status]) + '\n')

            # Присваиваем новый индекс
            with open(self.tmpdir+'/cars_index.txt', 'r') as file_car_index:
                lines = file_car_index.readlines()
                count_lines = len(lines)+1
            with open(self.tmpdir+'/cars_index.txt', 'a+') as file_car_index:
                file_car_index.write(
                    ", ".join([str(count_lines), new_vin]) + '\n')
        if car_index:
            return Car(vin=new_vin,
                       model=int(model),
                       price=Decimal(price),
                       date_start=datetime.strptime(
                           date_start, '%Y-%m-%d %H:%M:%S'),
                       status=CarStatus(status))
        return None

    # Задание 6. Удаление продажи
    def revert_sale(self, car_vin: str) -> Car:
        sales_index = None
        car_index = None
        if car_vin is not None:
            with open(self.tmpdir+'/sales_index.txt', 'r') as file_sales_index:
                lines_car = file_sales_index.readlines()
                # Поиск index
                for index, line in enumerate(lines_car):
                    list = line.strip().split(', ')
                    cv = list[1]
                    if cv == car_vin:
                        sales_index = int(list[0])
                        break
            if sales_index is not None:
                with open(self.tmpdir+'/sales.txt', 'r') as file_sales:
                    index_lines = file_sales.readlines()
                    # удаление
                del index_lines[sales_index - 1]
                with open(self.tmpdir+'/sales.txt', 'w') as file_sales:
                    file_sales.writelines(index_lines)
     
                with open(self.tmpdir+'/sales_index.txt', 'r') as file_sales:
                    index_lines = file_sales.readlines()
                    # удаление
                del index_lines[sales_index - 1]
                with open(self.tmpdir+'/sales_index.txt', 'w') as file_sales:
                    file_sales.writelines(index_lines)

            with open(self.tmpdir+'/cars_index.txt', 'r') as ci:
                index_lines = ci.readlines()
                # Поиск VIN в index
                for index, line in enumerate(index_lines):
                    # разбиваем строку на части по запятой и пробелу, возвращая список элементов.
                    list = line.strip().split(', ')
                    vin = list[1]  # Получаем второй элемент из списка
                    if vin == car_vin:
                        car_index = int(list[0])  # Присваиваем индекс
                        break  # Завершаем цикл, если нашли VIN
            if car_index is not None:
                with open(self.tmpdir+'/cars.txt', 'r') as ci:
                    lines_car = ci.readlines()
                    parts = lines_car[car_index - 1].strip().split(', ')

                # Изменяем статус автомобиля на 'available'
                lines_car[car_index - 1] = lines_car[car_index - 1].replace(
                    lines_car[car_index - 1].strip().split(', ')[-1], 'available')
        
                # Записываем изменения обратно в файл
                with open(self.tmpdir+'/cars.txt', 'w') as file_4:
                    file_4.writelines(lines_car)

                return Car(vin=str(car_vin),
                           model=int(parts[1]),
                           price=Decimal(parts[2]),
                           date_start=datetime.strptime(
                    parts[3], '%Y-%m-%d %H:%M:%S'),
                           status=CarStatus('available')
                )
        return None

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        dict_top = dict()
        with open(self.tmpdir+'/cars_index.txt', 'r') as file_car_index:
            index_lines = file_car_index.readlines()

            vin = None
            car_index = None

            for index, line in enumerate(index_lines):
                # разбиваем строку на части по запятой и пробелу, возвращая список элементов.
                list = line.strip().split(', ')
                vin = list[1]  # Получаем второй элемент из списка
                car_index = int(list[0])  # Присваиваем индекс

                with open(self.tmpdir+'/cars.txt', 'r') as file_4:
                    lines_car = file_4.readlines()

                    car = lines_car[car_index - 1]
                    parts = car.strip().split(', ')
                    model_id = int(parts[1])

                with open(self.tmpdir+'/models_index.txt', 'r') as file_model_index:
                    lines = file_model_index.readlines()
                    brand = ''
                    model_index = int(lines[model_id - 1].split(', ')[1])

                    if model_index is not None:
                        with open(self.tmpdir+'/models.txt', 'r') as file_model:
                            lines = file_model.readlines()

                            model = lines[model_index - 1]
                            parts = model.strip().split(', ')
                            model_name = parts[1]
                            brand = parts[2]

                with open(self.tmpdir + '/sales_index.txt', 'r') as file_sales_index:
                    lines = file_sales_index.readlines()

                    sales_index = None

                    for i, line in enumerate(lines):
                        si = line.strip().split(', ')
                        sales_list = si[1]
                        if sales_list == vin:
                            sales_index = int(si[0])
                            break
                    if sales_index is not None:
                        with open(self.tmpdir+'/sales.txt', 'r') as file_sales:
                            lines = file_sales.readlines()
                            parts = lines[sales_index - 1].split(', ')
                            price = Decimal(parts[2])
                            if model_name in dict_top:
                                cnt = dict_top[model_name][0]
                                old_cost = dict_top[model_name][1]
                                dict_top[model_name] = (
                                    cnt + 1, max(price, old_cost), brand)
                            else:
                                dict_top[model_name] = (1, price, brand)
        result = []
        if dict_top:
            data = dict_top.items()
            sorted_data = sorted(data, key=lambda x: (
                x[1][0], x[1][1]), reverse=True)
            total_data = sorted_data[0:3]
            for i in total_data:
                result.append(ModelSaleStats(model_name=i[0],
                                             brand=i[1][-1],
                                             sales_number=i[1][0]))
        return result
