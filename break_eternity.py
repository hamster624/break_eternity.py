# Made by the_hamster_god and my github is "https://github.com/hamster624".
# I have made a roblox calculator and a website calculator here they are web:"https://hamster624.github.io/ExpantaNum-Calculator/", and the roblox: "https://www.roblox.com/games/89516713438784/calculator".
# Special thanks to Wolframalpha for helping me with large powers and another special thanks to ExpantaNum.js because that's what i used for examples.
# kind of break_eternity.js but in py. That's not all i also got some formatters "hyper_e" and "format", "power10_tower". The limit is 10^^1e308.
# to use slog you just do slog(x) OR if you want you can define the base like this slog(x, base).
# addlayer(x,y) is just 10^x but y amount times if y isn't set then it's just 10^x.
# all total operation: slog, log, root, sqrt, div, sub, add, mul, addlayer, pow, fact, tetr.
# all function excluding operation: eq, lt, gt, format, hyper_e, power10_tower.
# also if you have any bugs report them in the github page
# i am not the same person who made break_eternity.js im just some random
import math

# --Editable constants--
FORMAT_THRESHOLD = 7 #the amount of e's when switching from scientific to (10^)^x format
format_decimals = 6 # amount of decimals for the "hyper-e" format, "format" and the "power10_tower" format. Keep below 16.
max_layer = 10 # amount of 10^ in power10_tower format when it switches from 10^ iterated times to 10^^x
# --End of editable constants--

LARGE_HEIGHT_THRESHOLD = 9007199254740991 # dont ask me why it's this, i just used it because ExpantaNum.js uses it

def get_sign_and_abs(x):
    if isinstance(x, (int, float)):
        if x < 0:
            return -1, -x
        else:
            return 1, x
    elif isinstance(x, str):
        if x.startswith('-'):
            return -1, x[1:]
        else:
            return 1, x
    else:
        return 1, x

def apply_sign(x, sign):
    if sign == 1:
        return x
    else:
        return negate(x)

def negate(x):
    if isinstance(x, (int, float)):
        if x == 0:
            return 0
        return -x
    elif isinstance(x, str):
        if x.startswith('-'):
            return x[1:]
        else:
            return '-' + x
    else:
        return '-' + str(x)

def compare_positive(a, b):
    if eq(a, b) == "True":
        return 0
    elif gt(a, b) == "True":
        return 1
    else:
        return -1

def tetration(a, h):
    try:
        h_float = float(h)
    except (TypeError, ValueError):
        return "Error: Tetration height must be a valid number below 1e308"
    
    if h_float < 0:
        return "Error: Tetration height can not be less than 0"
    try:
        a_float = float(a)
        use_float = True
    except (TypeError, ValueError):
        use_float = False
    
    if not use_float:
        if isinstance(a, str):
            s = slog(a)
            if math.isnan(s) or math.isinf(s):
                return "NaN"
            return tetration(10, s + h_float-1)
        else:
            return "NaN"
    a_float = float(a)
    if a_float < 0:
        return "NaN"
    if a_float == 0:
        if h_float == 0:
            return "NaN"
        return "0" if h_float % 2 == 0 else ("1" if h_float == 1 else "0")
    if a_float == 1:
        return "1"

    if h_float >= LARGE_HEIGHT_THRESHOLD:
        if abs(h_float - round(h_float)) < 1e-12:
            height_str = format_int_scientific(int(round(h_float)))
        else:
            height_str = format_float_scientific(h_float)
        return f"10^^{height_str}"

    log10a = math.log10(a_float)
    log_log10a = math.log10(log10a) if log10a > 0 else -float('inf')
    try:
        n = math.floor(h_float)
    except (ValueError,TypeError, OverflowError):
        return "NaN"
    f = h_float - n
    current = a_float ** f if f > 0 else 1.0
    layer = 0

    if n == 0:
        if current < 1e12:
            return current
        if abs(current - round(current)) < 1e-10:
            return str(format_float_scientific(round(current)))
        return f"{current:.15g}"

    n_remaining = int(n)
    layer0_iter = 0
    prev_current = current

    while n_remaining > 0:
        if layer == 0:
            if layer0_iter >= 10000:
                if abs(current - prev_current) < 1e-10:
                    break
                prev_current = current
                layer0_iter = 0

            next_log10 = current * log10a
            if next_log10 > 307.6536855:
                current = next_log10
                layer = 1
            else:
                try:
                    current = a_float ** current
                except (OverflowError, ValueError):
                    current = next_log10
                    layer = 1

            layer0_iter += 1
            n_remaining -= 1

        elif layer == 1:
            current = log_log10a + current
            layer += n_remaining
            n_remaining = 0

        else:
            layer += n_remaining
            n_remaining = 0

    if layer >= 1 and math.isfinite(current) and current > LARGE_HEIGHT_THRESHOLD:
        while current > LARGE_HEIGHT_THRESHOLD:
            current = math.log10(current)
            layer += 1

    if layer == 0:
        if current < 1e12:
            return current
        if math.isnan(current):
            return "NaN"
        if abs(current - round(current)) < 1e-10:
            return str(format_float_scientific(round(current)))
        return f"{current:.15g}"
    elif layer == 1:
        return f"e{current:.15g}"
    elif layer <= FORMAT_THRESHOLD:
        return 'e' * layer + f"{current:.15g}"
    else:
        return f"(10^)^{layer} {current:.15g}"

def slog_numeric(x, base):
    if base <= 0 or base == 1:
        return "NaN"
    if x < 0:
        return "NaN"
    count = 0.0
    current = x
    while current < 1:
        if current <= 0:
            return float('-Inf')
        try:
            current = base ** current
        except OverflowError:
            current = 0
        count -= 1
    while current > base:
        try:
            current = math.log(current, base)
        except (OverflowError, ValueError):
            return "NaN"
        count += 1
    try:
        frac = math.log(current, base)
    except (OverflowError, ValueError):
        return "NaN"
    return count + frac

def slog(x, base=10):
    sign_x, abs_x = get_sign_and_abs(x)
    if sign_x == -1:
        return "Error: x can't be a negative number"
    x = abs_x
    if x == 0:
        return -1
    if isinstance(x, str):
        if base == 10:
            if x.startswith("10^^"):
                try:
                    return float(x[4:])
                except:
                    return "NaN"
            elif x.startswith("(10^)^"):
                parts = x.split(' ', 1)
                if len(parts) < 2:
                    return "NaN"
                head, mantissa_str = parts
                k_str = head[6:]
                try:
                    k = int(k_str)
                    mantissa = float(mantissa_str)
                except:
                    return "NaN"
                return k + slog_numeric(mantissa, 10)
            else:
                count = 0
                s = x
                while s.startswith('e'):
                    count += 1
                    s = s[1:]
                if count == 0:
                    try:
                        return slog_numeric(float(x), 10)
                    except:
                        return "NaN"
                else:
                    try:
                        mantissa = float(s)
                    except:
                        return "NaN"
                    return count + slog_numeric(mantissa, 10)
        else:
            count = 0.0
            s = x
            while s:
                if s.startswith("10^^"):
                    height_str = s[4:]
                    try:
                        height = float(height_str)
                    except:
                        try:
                            return count + slog_numeric(float(s), base)
                        except:
                            return "NaN"
                    count += height
                    return count
                elif s.startswith("(10^)^"):
                    parts = s.split(' ', 1)
                    if len(parts) < 2:
                        try:
                            return count + slog_numeric(float(s), base)
                        except:
                            return "NaN"
                    head, mantissa_str = parts
                    k_str = head[6:]
                    try:
                        k = int(k_str)
                        mantissa = float(mantissa_str)
                    except:
                        return "NaN"
                    count += k
                    s = mantissa_str
                elif s.startswith('e'):
                    idx = 0
                    while idx < len(s) and s[idx] == 'e':
                        idx += 1
                    rest = s[idx:]
                    count += idx
                    s = rest
                else:
                    try:
                        return count + slog_numeric(float(s), base)
                    except:
                        return "NaN"
            return count
    else:
        return slog_numeric(x, base)

def log(x):
    sign_x, abs_x = get_sign_and_abs(x)
    if sign_x == -1:
        return "Error: Logarithm of negative number"
    x = abs_x
    if isinstance(x, str):
        if x == "NaN" or x.startswith("Error:"):
            return x
        if x.startswith("10^^"):
            height_str = x[4:]
            try:
                height = float(height_str)
                if height <= 1:
                    return "1" if height == 1 else "Error: Height <= 0"
                return "10^^" + str(height - 1)
            except:
                return "NaN"
        elif x.startswith("(10^)^"):
            parts = x.split(' ', 1)
            if len(parts) < 2:
                return "NaN"
            head, mantissa_str = parts
            k_str = head[6:]
            try:
                k = int(k_str)
                mantissa = float(mantissa_str)
            except:
                return "NaN"
            if k == 1:
                return str(mantissa)
            else:
                return f"(10^)^{k-1} {mantissa_str}"
        elif x.startswith('e'):
            count = 0
            s = x
            while s.startswith('e'):
                count += 1
                s = s[1:]
            if count == 1:
                return s
            else:
                return 'e' * (count - 1) + s
        else:
            try:
                num_val = float(x)
                return str(math.log10(num_val))
            except:
                return "NaN"
    else:
        try:
            return str(math.log10(x))
        except:
            return "NaN"

def addlayer(a, b=1):
    s = slog(a)
    if math.isinf(s) or math.isnan(s):
        return "NaN"
    try:
        return tetration(10, float(b) + float(s))
    except (ValueError, TypeError, OverflowError):
        return "Error trying to do ``addlayer``"
def is_float_convertible(x):
    try:
        float(x)
        return True
    except:
        return False

def subtract_positive(a, b, depth=0):
    MAX_DEPTH = 3
    if depth > MAX_DEPTH:
        return a
    if a in [0, "0"]:
        return negate(b)
    if b in [0, "0"]:
        return a
    if is_float_convertible(a) and is_float_convertible(b):
        a_float = float(a)
        b_float = float(b)
        result = a_float - b_float
        if result < 0:
            return negate(str(abs(result)))
        if result == 0:
            return 0
        if abs(result) < 1e-3 or abs(result) >= 1e12:
            return format_float_scientific(result)
        return str(result)
    if lt(a, b) == "True":
        return negate(subtract_positive(b, a, depth+1))
    if eq(a, b) == "True":
        return 0
    if isinstance(a, str) and a.startswith('e') and is_float_convertible(b):
        try:
            exponent = float(a[1:])
            if exponent > 1e2:
                a_val = 10 ** exponent
                if a_val > 1e100:
                    return a
            else:
                a_val = 10 ** exponent
            result = a_val - float(b)
            if result <= 0:
                return 0
            if result < 1e12:
                return result
            return "e" + str(math.log10(result))
        except:
            pass
            
    A = log(a)
    B = log(b)
    if A == "NaN" or B == "NaN":
        return a
    D = subtract_positive(A, B, depth+1)
    if D == "NaN" or D == "Error: Logarithm of negative number":
        return a
    try:
        D_float = float(D)
        if D_float > 1000:
            return a
        C = 10**D_float - 1
        if C <= 0:
            return 0
        log10C = math.log10(C)
        B_float = float(B)
        new_exp = B_float + log10C
        return "e" + str(new_exp)
    except:
        return a
def add_positive(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if a == 0:
            return b
        if b == 0:
            return a
        if a < 1e150 and b < 1e150:
            return a + b
    s_a = slog(a)
    s_b = slog(b)
    if math.isnan(s_a) or math.isnan(s_b):
        return "NaN"
    if abs(s_a - s_b) >= 1:
        return a if s_a > s_b else b
    if s_a > 100 or s_b > 100:
        return a if s_a >= s_b else b
    if s_a < 1 and s_b < 1:
        try:
            return float(a) + float(b)
        except:
            return a if s_a >= s_b else b
    if gt(b, a) == "True":
        a, b = b, a
        s_a, s_b = s_b, s_a
    log_a = log(a)
    log_b = log(b)
    try:
        if isinstance(log_a, (int, float)) and isinstance(log_b, (int, float)):
            d_val = log_b - log_a
        else:
            d_exp = subtract(log_b, log_a)
            d_val = float(d_exp) if is_float_convertible(d_exp) else -float('inf')
    except:
        d_val = -float('inf')
    if d_val < -350:
        return a
    try:
        x = 10.0 ** d_val
        y = math.log10(1 + x)
    except:
        return a
    if isinstance(log_a, (int, float)):
        new_exponent = log_a + y
    else:
        try:
            new_exponent = addition(log_a, y)
        except:
            return a
    return addlayer(new_exponent)

def addition(a, b):
    try:
        if float(a) and float(b) < 5e307:
            return float(a)+float(b)
    except (ValueError, TypeError, OverflowError):
        pass
    sign_a, abs_a = get_sign_and_abs(a)
    sign_b, abs_b = get_sign_and_abs(b)
    if abs_a in [0, "0"] and abs_b in [0, "0"]:
        return 0
    if abs_a in [0, "0"]:
        return apply_sign(abs_b, sign_b)
    if abs_b in [0, "0"]:
        return apply_sign(abs_a, sign_a)
    if sign_a == sign_b:
        result = add_positive(abs_a, abs_b)
        return apply_sign(result, sign_a)
    cmp = compare_positive(abs_a, abs_b)
    if cmp == 0:
        return 0
    elif cmp > 0:
        result = subtract_positive(abs_a, abs_b, 0)
        return apply_sign(result, sign_a)
    else:
        result = subtract_positive(abs_b, abs_a, 0)
        return apply_sign(result, sign_b)
def subtract(a, b):
    return addition(a, negate(b))

def multiply(a, b):
    try:
        if float(a)< 1e150 and float(b) < 1e150:
            return float(a) * float(b)
    except (TypeError, ValueError, OverflowError):
        pass
    try:
        return addlayer(add(log(a),log(b)))
    except:
        return "Error doing multiplication"    
def division(a, b):
    try:
        if a < "ee308" and b < "ee308":
            return addlayer(log(a)-log(b))
    except (ValueError, TypeError, OverflowError):
        pass
    if gt(a, b) == "True":
        return str(a)
    if eq(a, b) == "True":
        return "1"
    if lt(a, b) == "True":
        return "0"
    if b == 0 or b == "0":
        return "Error: Division by zero"
    try:
        addlayer(sub(log(a), log(b)))
    except:
        return "NaN"

def power(a,b):
    return addlayer(mul(log(a),b))

def root(a, b):
    if eq(log(a), b) == "True":
        return 10
    if lt(log(a), b) == "True":
        return 1
    if gt(a, "eeee308"):
        return str(a)
    else:
        return power(a, division(1, b))

def sqrt(x):
    return root(x, 2)
def factorial(n):
    sign, abs_x = get_sign_and_abs(n)
    try:
        if sign == -1:
            return "NaN"
        try:
            n = float(abs_x)
        except (TypeError, OverflowError, ValueError):
            n = str(abs_x)
        if abs_x != n:
            return "NaN"
    except:
        return "NaN"
    if n == 0:
        return 1
    try:
        if n < 170:
            return math.gamma(n+1)
    except (ValueError, TypeError, OverflowError):
        pass
    if gt(n, "e1000000000000") == "True":
        return addlayer(n, 1) # yes what you are seeing is that if the values is greater than e1000000000000 it just 10^x the number
    else:
        term1 = mul(add(n, 0.5), log(n))
        term2 = negate(mul(n, 0.4342944819032518))
        term3 = mul(0.5, log(6.2831853071795865))
        total_log = add(add(term1, term2), term3)
        return addlayer(total_log)
# Comparisons
def gt(a, b):
    sign_a, abs_a = get_sign_and_abs(a)
    sign_b, abs_b = get_sign_and_abs(b)
    if sign_a != sign_b:
        return "True" if sign_a > sign_b else "False"
    if sign_a == 1:
        a_slog = slog(abs_a)
        b_slog = slog(abs_b)
        if math.isnan(a_slog) or math.isnan(b_slog):
            return "False"
        if a_slog > b_slog:
            return "True"
        elif a_slog < b_slog:
            return "False"
        else:
            if is_float_convertible(abs_a) and is_float_convertible(abs_b):
                return "True" if float(abs_a) > float(abs_b) else "False"
            else:
                return "False"
    else:
        a_slog = slog(abs_a)
        b_slog = slog(abs_b)
        if math.isnan(a_slog) or math.isnan(b_slog):
            return "False"
        if a_slog < b_slog:
            return "True"
        elif a_slog > b_slog:
            return "False"
        else:
            if is_float_convertible(abs_a) and is_float_convertible(abs_b):
                return "True" if float(abs_a) < float(abs_b) else "False"
            else:
                return "False"

def lt(a, b):
    return "True" if gt(b, a) == "True" else "False"

def eq(a, b):
    sign_a, abs_a = get_sign_and_abs(a)
    sign_b, abs_b = get_sign_and_abs(b)
    if sign_a != sign_b:
        return "False"
    try:
        a_slog = slog(abs_a)
        b_slog = slog(abs_b)
    except:
        return "False"
    if math.isnan(a_slog) or math.isnan(b_slog):
        return "False"
    if abs(a_slog - b_slog) > 1e-10:
        return "False"
    if is_float_convertible(abs_a) and is_float_convertible(abs_b):
        return "True" if abs(float(abs_a) - float(abs_b)) < 1e-10 else "False"
    return "False" 
# Short names
def fact(x):
    return factorial(x)
def pow(a, b):
    return power(a, b)

def tetr(a, h):
    return tetration(a, h)

def mul(a, b):
    return multiply(a, b)

def add(a, b):
    return addition(a, b)

def sub(a, b):
    return subtract(a, b)

def div(a, b):
    return division(a, b)
# Formats
def hyper_e(tet, decimals=format_decimals):
    if isinstance(tet, (int, float)):
        return comma_format(tet, decimals)
    tet_str = str(tet)
    if tet_str.startswith("10^^"):
        height = tet_str[4:]
        return f"E10#{height}"
    if tet_str.startswith("(10^)^"):
        parts = tet_str.split(' ', 1)
        if len(parts) == 2:
            head, mant = parts
            try:
                layers = int(head[6:])
                return f"E{mant}#{layers+1}"
            except ValueError:
                pass
    idx = 0
    while idx < len(tet_str) and tet_str[idx] == 'e':
        idx += 1
    if idx > 0:
        mant_str = tet_str[idx:]
        try:
            mant_val = float(mant_str)
            if idx > 1:
                return f"E{comma_format(mant_val, decimals)}#{idx}"
            else:
                return f"E{comma_format(10**mant_val, decimals)}"
        except ValueError:
            pass
    return tet_str

def format(tet, decimals=6):
    if isinstance(tet, (int, float)):
        return comma_format(tet, decimals)
    tet_str = tet
    if tet_str.startswith("10^^"):
        height = float(tet_str[4:])
        return f"F{comma_format(height, 6)}"
    try:
        val = float(tet_str)
        if abs(val) < 1e308:
            return comma_format(val, decimals)
    except ValueError:
        pass
    if tet_str.startswith("(10^)^"):
        parts = tet_str.split(' ', 1)
        if len(parts) == 2:
            head, mant = parts
            try:
                layers = int(head[len("(10^)^"):])
                mant_val = float(mant)
                if abs(mant_val - 1e10) < 1e-5:
                    return f"F{comma_format(layers + 2, 6)}"
                elif mant_val < 10:
                    return f"{mant_val:.{decimals}f}F{comma_format(layers, 0)}"
                elif mant_val < 1e10:
                    return f"{math.log10(mant_val):.{decimals}f}F{comma_format(layers + 1, 0)}"
                else:
                    return f"{math.log10(math.log10(mant_val)):.{decimals}f}F{comma_format(layers + 2, 0)}"
            except ValueError:
                pass
    if tet_str.startswith('e'):
        idx = 0
        while idx < len(tet_str) and tet_str[idx] == 'e':
            idx += 1
        rest = tet_str[idx:]
        exp_pos = rest.rfind('e')
        if exp_pos > 0:
            mant_str = rest[:exp_pos]
            exp_str = rest[exp_pos+1:]
            try:
                mant_f = float(mant_str)
                exp_i = int(exp_str)
                return f"{'e'*idx}{comma_format(mant_f, decimals)}e{comma_format(exp_i, 0)}"
            except ValueError:
                pass
        try:
            mant = float(rest)
            return f"{'e'*idx}{comma_format(mant, decimals)}"
        except ValueError:
            pass
    return tet_str
def power10_tower(tet, max_layers=max_layer, decimals=format_decimals):
    try:
        if float(tet) < 1e308:
            return tet
    except (ValueError, TypeError, OverflowError):
        pass
    tet = slog(tet)
    if math.isnan(tet) or math.isinf(tet):
        return "NaN"
    if tet > max_layers:
        return "10^^" + str(tet)
    height = int(math.floor(tet))
    frac   = tet - height
    if height <= 0:
        return frac
    mant = addlayer(frac,2)
    expr = comma_format(float(mant), decimals)
    for _ in range(height - 1):
        expr = f"10^{expr}"
    return expr
# Useless formats only used for this code
def comma_format(number, decimals=format_decimals):
    if abs(number) < 1e-3 or abs(number) >= 1e12:
        s = f"{number:.{decimals}e}"
        if 'e' in s:
            mant, exp = s.split('e')
            exp = exp.lstrip('+').lstrip('0') or '0'
            return f"{mant}e{exp}"
        return s
    return f"{number:,.{decimals}f}"

def default_format(tet_str: str) -> str:
    return tet_str

def format_int_scientific(n: int, sig_digits: int = 16) -> str:
    s = f"{n:.{sig_digits}e}"
    mant, exp = s.split('e')
    mant = mant.rstrip('0').rstrip('.')
    exp = exp.lstrip('+').lstrip('0') or '0'
    return f"{mant}e{exp}"

def format_float_scientific(x: float, sig_digits: int = 16) -> str:
    if x <= 0 or math.isinf(x) or math.isnan(x):
        return f"{x}"
    exp = math.floor(math.log10(x))
    mant = x / (10 ** exp)
    mant_str = f"{mant:.{sig_digits}g}".rstrip('0').rstrip('.')
    return f"{mant_str}e{exp}"
# The end of break_eternity.py
# this is around 1 second of computation time which means if you are only doing this 1 expression you are going to get 7420 fps
import time
start_time = time.perf_counter()
i= 10000
for _ in range(1, 7420):
    tetr(10,addlayer(slog(fact(div(sqrt(mul(2, tetr(i, add(i, slog(tetr(11,log(i))))))), pow(sub(tetr(i,i), tetr(i,sub(i,0.5))),i)))), log(slog(i))))
end_time = time.perf_counter()
print(end_time-start_time)
#print(slog("(10^)^1003 11140.3094437414"))
#print(tetr("eee11",2.5))
#print(tetr("eee12",2.23))
#print(tetr("eee6", 1.25))
#print(tetr("ee10",1.9))
#print(tetr("e100000000000", 1.003))
#print(tetr("eee10",1.9))
#print(tetr("eeee10",2))
#print(tetr("(10^)^1003 11140.3094437414", 2))
# if you are going to use a online python thing delete this code after this msg that code is for the ui and sadly i dont think any online python thing can do ui
import tkinter as tk
from tkinter import ttk
def open_tetr_window():
    w = tk.Toplevel(root)
    w.title("Evaluate Expression")
    w.resizable(False, False)

    ttk.Label(w, text="Expression:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    expr_entry = ttk.Entry(w, width=40)
    expr_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(w, text="Format:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    formats = {
        "best format": format,
        "hyper-e": hyper_e,
        "default": default_format,
        "power10_tower": power10_tower,
    }
    fmt_var = tk.StringVar(value="best format")
    fmt_menu = ttk.Combobox(w, textvariable=fmt_var, values=list(formats.keys()), state="readonly", width=12)
    fmt_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(w, text="Result:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    res_var = tk.StringVar()
    result_entry = ttk.Entry(w, textvariable=res_var, width=40, state="readonly")
    result_entry.grid(row=2, column=1, padx=5, pady=5)

    def evaluate_expression():
        expr = expr_entry.get()
        fmt_func = formats.get(fmt_var.get(), format)
        safe_globals = {
            "__builtins__": {},
            "math": math,
            "tetration": tetration,
            "tetr": tetration,
            "fact": fact,
            "factorial": factorial,
            "slog": slog,
            "addlayer": addlayer,
            "add": add,
            "addition": addition,
            "sub": sub,
            "subtract": subtract,
            "mul": mul,
            "multiply": multiply,
            "div": div,
            "division": division,
            "pow": pow,
            "power": power,
            "root": root,
            "sqrt": sqrt,
            "eq": eq,
            "lt": lt,
            "gt": gt,
            "log": log,
        }

        try:
            result = eval(expr, safe_globals)
            formatted = fmt_func(result)
        except Exception as e:
            formatted = f"Error: {e}"
        
        res_var.set(formatted)
        w.after(20, evaluate_expression) 
    
    evaluate_expression()
    w.grab_set()
root = tk.Tk()
open_tetr_window()
root.withdraw()
root.mainloop()

# some random tetrstion examples and the expected is taken from expantanum.js
examples = [
    (2.1, 5, "8.888914407966787e27356134615"),
    (3.1, 5, "eee16.083046571057043"),
    (46, 3, "e5.10139e76"),
    (5, 5.6, "eeee47.74304417479632"),
    (6, 6.7, "eeeee415.41521734939835"),
    (5, 5.1, "eee29744.075716284777"),
    (5, 5.2, "eee1922647.9442190705"),
    (5, 5.3, "eee2158141736.8084674"),
    (5, 5.4, "eee643767002033583.4"),
    (5, 5.5, "eeee25.39516912476743"),
    (5.1, 5.1, "eee46149.804097003005"),
    (5.2, 5.1, "eee72136.0960629602"),
    (10, 10, "(10^)^8 10000000000"),
    (10, 11, "(10^)^9 10000000000"),
    (10, 11.5, "(10^)^10 1453.0403018990435"),
    (10, 11.6, "(10^)^10 9573.521248329678"),
    (1e300, 323473, "(10^)^323473 302.4771212547197"),
    (1e15, 2, "e1.5000000000000004e16"),
    (2, 10000000, "(10^)^9999996 19727.780405607016"),
    (10, 10000000000000000, "10^^1e16"),
    (10, 100000000000000000, "10^^1e17"),
    (10, 24376523406734064537, "10^^2.4376523406734036e19"),
    (64, 1e300, "10^^1e300"),
    (2, 1000, "(10^)^996 19727.780405607016"),
    (3, 1000, "(10^)^997 3638334640023.7783"),
    (4, 1000, "(10^)^998 153.90699754796802"),
    (5.1, 1000, "(10^)^998 2873.126246131205"),
    (6, 1000, "(10^)^998 36305.31580191892"),
    (7, 1000, "(10^)^998 695974.5020745555"),
    (8, 1000, "(10^)^998 15151335.734932054"),
    (9, 1000, "(10^)^998 369693099.6112291"),
    (10, 1000, "(10^)^998 10000000000"),
    (6437347,2437435756856845236347, "10^^2.4374357568568414e21"),
]
#for base, height, expected in examples:
#     result = tetration(base, height)
#     print(f"{base}^^{height} = {result} expected {expected}")
# uncomment the next comments for the examples
# some random test examples i was doing to make sure everything works perfectly
print(add("(10^)^10 10","(10^)^10 10"))
print(gt("eee10", "ee10"))
print(lt("eee10", "ee10"))
print(eq("eee10", "ee10"))
print(tetration(1e45,10.2))
print(tetration(10,1.5))
print(slog("eeee74585"))
print(pow(2,1024))
print(mul(10, slog(int(2**1024))))
print(tetration(pow(2,1023.9), pow(2,1023.9)))
print(slog(2**1024))
print(format(tetration(pow(2,1023.9), pow(2,1023.9))))
print(pow("(10^)^10 10", "(10^)^10 10"))
print(mul("ee30","ee30"))
print(log("ee30"))
print(mul(2,1024))
print(add("eeee345709","eee308456989"))
print(mul(10,10))
print(add(1e308,1e308))
print(pow(2,10200))
print(mul(log(10), 1024))
print(pow("e309","e309"))
print(mul("e30846585","e3088569"))
print(pow(tetration(10,5.37543),tetration(10,6.24623)))
expression = 'slog(pow(pow(tetration(slog(tetration(654.6234, 646.535)), slog(tetration(525.624,25.2))), slog("eee10")), pow("(10^)^11 535", "(10^)^10 634")))'
result = slog(pow(pow(tetration(slog(tetration(654.6234, 646.535)), slog(tetration(525.624,25.2))), slog("eee10")), pow("(10^)^11 535", "(10^)^10 634")))
print(f"{expression} = {result}")
print(addlayer("ee10"))
print(gt("10^^10","1e10"))
expression2 = 'power10_tower(tetr(6346,6))'
result2 = power10_tower(tetr(6346,6))
print(f"{expression2} = {result2}")
print(power10_tower(tetr(6346,6)))
print(tetr(2,2))
print(slog(1e12))

print(mul("ee10",0.5))
print(subtract("eee10","eeee10"))
# Test cases
print(subtract(1000, 1))       # 999
print(subtract(10, 9.9))       # 0.1
print(subtract("ee10", "ee9")) # "ee10" (negligible subtraction)
print(subtract("ee10", "ee10")) # 0 (equal values)
print(subtract("(10^)^10 10", "(10^)^10 10")) # 0
print(subtract("e5", "e4.999")) # Should compute difference (small residual)
print(subtract("e5", 1000))    # "e5" (different layers)
print(subtract("1e100", "5e99"))  # 5e+99
print(subtract("1e10", "1e10"))   # 0
print(subtract("ee10", "ee9"))    # ee10 (dominant term)
print(subtract("e1000", "e1001"))  # e999.0 (after exponent subtraction)
print(division("e1000", "e500"))
print(sqrt("eee10"))
print(root("eeeee10", "eeee309"))
print(mul("eee10",0.5))
print(fact(1000))
print(mul(0.5, log(mul(2, math.pi))) )