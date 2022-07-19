from typing import List

from ..models import Prefecture, City, Address


def data_to_city(data: List[str]) -> City:
    pref_length = len(Prefecture.__annotations__)
    pref = Prefecture(*data[:pref_length])
    city = City(int(data[pref_length]), pref, *data[pref_length + 2:])
    return city


def data_to_address(data: List[str]) -> Address:
    pref_length = len(Prefecture.__annotations__)
    city_length = len(City.__annotations__)
    city = data_to_city(data[:pref_length + city_length])
    address = Address(int(data[pref_length + city_length]), city, *data[pref_length + city_length + 2:])
    return address
