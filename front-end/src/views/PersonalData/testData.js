export const data = {
  tableData: [...Array(2)].map(() => ({
    fullName: {
      columnName: "ФИО",
      secondName: {
        value: "Ivanov",
        columnName: "Фамилия"
      },
      firstName: {
        value: "Ivan",
        columnName: "Имя"
      },
      patronymic: {
        value: "Ivanovich",
        columnName: "Отчество"
      }
    },
    birthday: {
      value: "03-12-1999",
      columnName: "День рождения"
    },
    motherFullName: {
      columnName: "ФИО матери",
      secondName: {
        value: "Ivanov",
        columnName: "Фамилия матери"
      },
      firstName: {
        value: "Ivan",
        columnName: "Имя матери"
      },
      patronymic: {
        value: "Ivanovich",
        columnName: "Отчество матери"
      }
    },
    fatherFullName: {
      columnName: "ФИО отца",
      secondName: {
        value: "Ivanov",
        columnName: "Фамилия отца"
      },
      firstName: {
        value: "Ivan",
        columnName: "Имя отца"
      },
      patronymic: {
        value: "Ivanovich",
        columnName: "Отчество отца"
      }
    }
  })),
  tableStructure: {
    fullName: {
      columnName: "ФИО",
      secondName: {
        columnName: "Фамилия"
      },
      firstName: {
        columnName: "Имя"
      },
      patronymic: {
        columnName: "Отчество"
      }
    },
    birthday: {
      columnName: "День рождения"
    },
    motherFullName: {
      columnName: "ФИО матери",
      secondName: {
        columnName: "Фамилия матери"
      },
      firstName: {
        columnName: "Имя матери"
      },
      patronymic: {
        columnName: "Отчество матери"
      }
    },
    fatherFullName: {
      columnName: "ФИО отца",
      secondName: {
        columnName: "Фамилия отца"
      },
      firstName: {
        columnName: "Имя отца"
      },
      patronymic: {
        columnName: "Отчество отца"
      }
    }
  }
}