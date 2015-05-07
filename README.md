#墨菲斯托(Mephisto)地理引擎

v0.0.1

墨菲斯托引擎提供大量地理事件的计算支持，运行于python3平台。

##参考内容

###类功能

墨菲斯托引擎提供一个日期类Date和一个时间类Time。
地理坐标方面提供一个经度类Longitude和一个纬度类Latitude已经一个地点类Location。
天体方面提供一个地球类Earth

####日期类Date
日期类在构造时可使用字符串（"2015-1-1"），或数字，或另一个Date实例。

对时间获取和赋值的成员函数：

```python

def get_date_tuple(self):

def set_date_string(self, date_string):

def get_date_string(self):

def set_date_number(self, date_number):

def get_date_number(self):

```

对日期分隔符的设置和获取：

```python
def set_sep_string(self, sep_string):

def get_sep_string(self):
```

对日期的移动操作：

```python

def forward_day(self, day):

def backward_day(self, day):

def forward_month(self, month):

def backward_month(self, month):

def forward_year(self, year):

def backward_year(self, year):

```


####时间类Time

####经度类Longitude

####纬度类Latitude

####地点类Location

####地球类Earth
