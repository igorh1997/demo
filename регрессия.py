import pandas as pd
import xlrd
from itertools import chain
import xlwt
import openpyxl
import xlsxwriter
import numpy as np
from cvxopt.modeling import variable, op
 
 
def equation_system_generator(z, y):
    z = z * 2
    p = []
    for k in range(0, y * 2):
            if(k >= y):
                per = "(x[0]"
                for i in range(1, z):
                    if (i < (z/2)):
                        per += "+ float(X"+"[" + str(k - y) + "]" + "[" + str(i - 1) + "])*x" + "[" + str(i) + "]"
                    if(i == (z / 2)):
                        if(k >= y):
                            per += " + (1 - h)*(" + "x[" + str(i) + "]"
                        else:
                            per += " - (1 - h)*(" + "x[" + str(i) + "]"
 
                             
                    if(i > (z / 2) and i < z - 1):
                         per += " + float(X" + "[" + str(k - y) + "]" + "[" + str((i - 1) - int(z / 2)) + "])*x[" + str(i) + "]"
                    if(i == (z - 1)):
                        if(k >= y):
                            per += " + float(X" + "[" + str(k - y) + "]" + "[" + str((i - 1) - int(z / 2))+"])*x[" + str(i) + "]))" + " >= " + "float(X" + "[" + str(k - y) + "]" + "[" + str(i - int(z / 2)) + "])"
                        else:
                            per += " + float(X" + "[" + str(k - y) + "]" + "[" + str((i - 1) - int(z / 2)) + "])*x[" + str(i) + "]))" + " <= " + "float(X" + "[" + str(k - y) + "]" + "[" + str(i - int(z / 2)) + "])"
 
            else:   
                per = "(x[0]"
                for i in range(1, z):
                    if (i < (z / 2)):
                        per += "+ float(X" + "[" + str(k) + "]" + "[" + str(i - 1) + "])*x" + "[" + str(i) + "]"
                    if(i == (z / 2)):
                        if(k >= y):
                            per += " + (1 - h)*(" + "x[" + str(i) + "]"
                        else:
                            per += " - (1 - h)*(" + "x[" + str(i) + "]"
 
 
                     
                    if(i > (z / 2) and i < z - 1):
                        per += " + float(X" + "[" + str(k) + "]" + "[" + str((i - 1) - int(z / 2)) + "])*x[" + str(i) + "]"
                    if(i == (z - 1)):
                        if(k >= y):
                            per += " + float(X" + "[" + str(k) + "]" + "[" + str((i - 1) - int(z / 2)) + "])*x[" + str(i) + "]))" + " >= " + "float(X" + "[" + str(k) + "]" + "[" + str(i - int(z / 2)) + "])"
                        else:
                            per += " + float(X" + "[" + str(k) + "]" + "[" + str((i - 1) - int(z / 2)) + "])*x[" + str(i) + "]))" + " <= " + "float(X" + "[" + str(k) + "]" + "[" + str(i - int(z / 2)) + "])"
            p.append(eval(per))
 
    for i in range(int(z / 2)):
        Z = "(x[" + str(i + int(z / 2)) + "]) >= 0"
        p.append(eval(Z))
    print("\n\n", p, "\n\n")
    return p
 
 
def target_function_generator(number_of_columns):
    target_function = "( N*x[" + str(number_of_columns) + "]"
    for i in range(1, int(number_of_columns)):
        target_function += "+x[" + str(i + int(number_of_columns)) + "]*float(X_sum[" + str(i - 1) + "])"
    target_function += ")"
    print(target_function)
    return eval(target_function)
     
 
def date_list_generator():
    beginning_of_period = 1996
    end_of_period = 2017
    years = []  
    for i in range((end_of_period + 1) - beginning_of_period):
      years.append(i + beginning_of_period)
    return(years)
 
 
def converter_of_multidimensional_lists_to_oneDimensional(temp_list):
    for ele in temp_list:
        if type(ele) == list:
            converter_of_multidimensional_lists_to_oneDimensional(ele)
        else:
            new_list.append(ele)
 
 
def coefficient_generator(name_of_indicators):
    number_of_indicators = len(name_of_indicators)
    fuzzy_odds = []
    classic_odds = []
    for i in range(number_of_indicators):
        fuzzy_odds.append('a' + str(i))
        classic_odds.append('r' + str(i))
    odds = ['h'] + fuzzy_odds + classic_odds + ['f']
    return(odds)
 
 
def coefficient_name_generator(name_of_indicators):
    name_of_indicators = name_of_indicators[:-1]
    fuzzyness = "нечеткость"
    free_member = "свободный член"
    function_value = "значение функции"
    name_of_indicators = [fuzzyness]+[free_member]+name_of_indicators+[free_member]+name_of_indicators+[function_value]
    return(name_of_indicators)
  
 
file = 'tsst2.xlsx'
 
# на это число делится h в цикле что бы смотреть на разлчные уровни нечёткости
 
the_number_of_parts_into_which_the_confidence_level_is_split = 10
m = 8 # Колличество столбцов  необходимых для конечного ответа
# m=0 - хранит в себе значение уровня нечеткости
# m=1 - хранит себе значение четких коэффициентов
# m=2 - хранит в себе значение нечетких коэффициентов
# m=3 - хранит в себе значение целевой функции
# m=4 - хранит в себе значение центральной прямой нашей модели
# m=5 - хранит в себе значение верхней прямой нашей модели
# m=6 - хранит в себе значение нижней прямой нашей модели
# m=7 - хранит в себе значение прямой содержащей реальные данные
list_to_answer = [[0] * m for i in range(the_number_of_parts_into_which_the_confidence_level_is_split)]
list_for_the_final_answer = []
work_excel_file = pd.ExcelFile(file)
worksheet_names = work_excel_file.sheet_names
 
for worksheet_name in worksheet_names:
    raw_dataframe = work_excel_File.parse(worksheet_name)
    X = raw_dataframe.to_numpy()
    dimension = X.shape
    the_number_of_rows_before_the_creation_of_the_control_sample = dimension[0]е
    number_of_indicators = dimension[1]
  # уберем последние 4 значения из строк для того что бы они участвовали в проверке адекватности модели
    the_number_of_rows_after_the_creation_of_the_control_sample = the_number_of_rows_before_the_creation_of_the_control_sample - 4
   # данная переменная учавствует в работе генератора системы уравнений и я не уверен можно ли её убирать так что пусть будет
    N = the_number_of_rows_after_the_creation_of_the_control_sample
  #сумма стоблцов показателей
    X_sum = []
    for i in range(int(number_of_indicators - 1)):
        z = 0
        for j in range(int(the_number_of_rows_after_the_creation_of_the_control_sample)):
            z += X[j][i]
        X_sum.append(z)
 
    # посчитаем модель с учётом различной нечеткости от 0 до 0.9 с шагом 0.1
    for h in range(the_number_of_parts_into_which_the_confidence_level_is_split):
    # на данном шаге заведём новую переменную для того что бы сохранить перменную h которая будет нужна для того что бы
    # заносить данные в нужные места в цикле ( что будет продемонстрированно далее)
        hh = h
    # переменная h теперь будет пробегать значения от 0 до 0.9 с шагом 0.1 а переменная hh будет пробегать значения от 0 до 9
        h = h / the_number_of_parts_into_which_the_confidence_level_is_split
    # введем переменную для того что бы проверить не выходят ли реальные данные за рамки построенные моделью
        test = 0
    # заводим переменную x в два раза больше чем колличество столбцов ведь в задаче линейного программирования
    # для нечеткой регрессии ограничений необходимо в два раза больше чем переменных
        x = variable(number_of_indicators * 2, 'x')
        problem = op(target_function_generator(number_of_indicators), equation_system_generator(number_of_indicators,the_number_of_parts_into_which_the_confidence_level_is_split))
        problem.solve(solver = 'glpk') 
        problem.status
        objective_function_value = (problem.objective.value()[0])
 
        classic_odds = []
        fuzzy_odds = []
        for i in range(number_of_indicators):
            classic_odds.append(x.value[i])
        for i in range(number_of_indicators,int(number_of_indicators) * 2):
            fuzzy_odds.append(x.value[i])
     
        list_to_answer[hh][0] = h
        list_to_answer[hh][1] = classic_odds
        list_to_answer[hh][2] = fuzzy_odds
        list_to_answer[hh][3] = objective_function_value
 
 
        # возвращаем 4 строки обратно так как график нам нужен по всей выборке
        the_number_of_rows_required_to_validate_the_model = the_number_of_rows_before_the_creation_of_the_control_sample
 
 
        ########################
        #####реальные данные####
        ########################
        realY = []
         
 
        for j in range(the_number_of_rows_required_to_validate_the_model):
            realY.append(X[j][number_of_indicators - 1])
          
    
        list_to_answer[hh][7] = realY
        ##########################
        ###центральные данные#####
        ##########################
        dotY = []
         
 
        for j in range(the_number_of_rows_required_to_validate_the_model):
            zz = classic_odds[0]
            for i in range(1, int(len(classic_odds))):
                zz += classic_odds[i] * X[j][i - 1]
            dotY.append(zz)
 
 
        list_to_answer[hh][4] = dotY
        #######################
        ###вверхние данные#####
        #######################
        dotY_right = []
 
 
        for j in range (the_number_of_rows_required_to_validate_the_model):
            z = classic_odds[0] + fuzzy_odds[0]
            for i in range(1, int(len(classic_odds))):
                z += (classic_odds[i] + fuzzy_odds[i]) * X[j][i - 1]
            dotY_right.append(z)
  
 
        list_to_answer[hh][5] = dotY_right
        #######################
        ###нижние   данные#####
        #######################
        dotY_left = []
  
 
        for j in range (the_number_of_rows_required_to_validate_the_model):
            z = classic_odds[0] - fuzzy_odds[0]
            for i in range(1, int(len(classic_odds))):
                 z += (classic_odds[i] - fuzzy_odds[i]) * X[j][i - 1]
            dotY_left.append(z)
      
         
        list_to_answer[hh][6] = dotY_left
 
 
        for i in range(the_number_of_rows_required_to_validate_the_model):
            if ((realY[i] >= dotY_left[i]) and (realY[i] <= dotY_right[i])):
                test = 1 
            else:
                test = 0
                break
        if test == 1:
            list_for_the_final_answer.append(list_to_answer[hh])
   
   
 
 
    name_export_file = worksheet_name + '.xlsx'
    writer = pd.ExcelWriter(name_export_file,engine = 'xlsxwriter')
    for i in range(the_number_of_parts_into_which_the_confidence_level_is_split - 1):
 
        # так как мне захотелось сделать лист листов то в следствии от него пришлось избавляться
        old_list = list_for_the_final_answer[i + 1][0:4]
        new_list = []
 
     
 
        converter_of_multidimensional_lists_to_oneDimensional(old_list)
        list_with_data = pd.DataFrame({'года': date_list_generator(),
                            'верхняя часть интервала': list_for_the_final_answer[i + 1][5],
                            'центральная часть интервала': list_for_the_final_answer[i + 1][4],
                            'нижняя часть интервала': list_for_the_final_answer[i + 1][6],
                            'Реальные данные':list_for_the_final_answer[i + 1][7]})
     
        list_with_names = pd.DataFrame({'Названия показателей': coefficient_name_generator(list(raw_dataframe)),
                             'Условные обозначения': coefficient_generator(list(raw_dataframe)),
                             'коэффициенты': new_list})
     
        list_with_data.to_excel(writer, sheet_name = "данные при h" + str(i + 1))
        list_with_names.to_excel(writer, sheet_name = "коэффициенты при h" + str(i + 1))
    writer.save()