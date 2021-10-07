import time
import datetime
from support_module import RefList
from support_module import get_table
from support_module import Table

if __name__ == '__main__':
    if (datetime.datetime.today().weekday() != 5) and (datetime.datetime.today().weekday() != 6):
        world = RefList('ММВБ+РТС+DowJonsIA+S&P500')
        err_counter = 0
        table = None

        while err_counter < 5:
            try:
                table = get_table(world)
            except ConnectionError:
                print(f'Connection Error {err_counter}')
                time.sleep(180)
                err_counter += 1
            else:
                break

        chart = Table(table)
        chart.add_to_graphs()
        chart.check_target_buy(100)
        chart.check_target_sell(100)
        chart.check_target_buy(90)
        chart.check_target_sell(90)
        chart.check_target_buy(80)
        chart.check_target_sell(80)
