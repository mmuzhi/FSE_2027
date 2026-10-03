def main():
    directions_opposite = {
        "N": "S",
        "E": "W",
        "W": "E",
        "S": "N",
        "NE": "SW",
        "NW": "SE",
        "SE": "NW",
        "SW": "NE"
    }
    
    D = input().strip()
    print(directions_opposite[D])

if __name__ == '__main__':
    main()