100 200

func haa(x, n) x + n * 5

rfunc draw(x, y, n)
    0 drawLine(x, y, x, haa(y, 1), 0, 0, 0)
    r drawLine(haa(x, n), y, haa(x, n), haa(y, n + 1), 0, 0, 0)

func main() draw(1, 1, 5)

