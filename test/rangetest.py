
range = []
min = '2018-10'
max = '2019-09'
#max = '2022-08'

print(f"{min} -> {max}")

min_year, min_month = int(min[:4]), int(min[5:])
max_year, max_month = int(max[:4]), int(max[5:])

year, month = min_year, min_month
range.append(f"{year:04}-{month:02}")
while year*100 + month < max_year*100 + max_month:
  month += 1
  if month == 13:
    month = 1
    year += 1
  range.append(f"{year:04}-{month:02}")

print(range)

range = [ d for d in range if d >= '2019-01' and d <= '2019-05' ]

print(range)

