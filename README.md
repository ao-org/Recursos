# ⚒️🔨 Assets / Recursos 🏹🪓
Recursos del cliente y servidor de Argentum Online

# Important Notice:
Before utilizing these assets, it is crucial that you thoroughly review the license terms. For detailed information on usage rights and restrictions, please consult the [license.txt](license.txt) file. Your understanding and adherence to these terms ensure the respectful and lawful use of these resources.

# What are we not sharing?
Although configuration files (such as DATs, INIs, graphics, etc.) can be freely adjusted by anyone, the resource repository is fully functional to ensure all game features work smoothly. However, configuration values, like object positions on maps, weapon statistics, and spell balance, can be customized. This allows for flexibility while maintaining the core structure of the game intact.

## Por favor considera apoyarnos en https://www.patreon.com/nolandstudios 

# Visual Basic 6 Code Standards (Argentum Online)

## 1. Mandatory use of `Call` and parentheses

* Always use `Call` when invoking any `Sub`.
* Always include parentheses, even if there are no arguments.

```vb
Call GuardarDatos()
Call EnviarMensaje("Hola", 2)
```

## 2. Functions always with parentheses

* Even when ignoring the return value, functions must be called with parentheses.

```vb
Call ObtenerTiempoActual()
Dim puntos As Long
puntos = CalcularPuntos(usuarioId)
```

## 3. Naming conventions

| Element        | Convention              | Example                   |
| -------------- | ----------------------- | ------------------------- |
| Modules        | `mod` prefix            | `modNetwork`, `modLogin`  |
| Forms          | `frm` prefix            | `frmMain`, `frmLogin`     |
| Controls       | Hungarian notation      | `txtNombre`, `lblError`   |
| Variables      | `camelCase`             | `userIndex`, `goldAmount` |
| Constants      | `PascalCase` or `UPPER` | `MaxItems`, `GOLD_PRICE`  |
| Functions/Subs | `PascalCase`            | `Call ValidarUsuario()`   |
| Enums          | `e_` prefix             | `e_TipoPago`              |

## 4. Spacing and formatting

* Use 4-space indentation.
* One blank line between procedures.
* Align related variable declarations:

```vb
Dim userGold    As Long
Dim userSilver  As Long
Dim userName    As String
```

## 5. Avoid magic numbers

* Declare all fixed values as constants in shared modules.

```vb
Public Const GOLD_PRICE As Long = 50000

If .Stats.GLD < GOLD_PRICE Then
    Call EscribirError("No tenés suficiente oro.")
End If
```

## 6. Standardized error handling

* Always use `On Error GoTo Name_Err` with a label at the end of the `Sub`.

```vb
Private Sub ValidarSesion()
    On Error GoTo ValidarSesion_Err

    Call HacerAlgo()

    Exit Sub

ValidarSesion_Err:
    Call TraceError(Err.Number, Err.Description, "modLogin.ValidarSesion", Erl)
End Sub
```

## 7. Modularization and reusability

* Group functionality into themed modules:

  * `modUser`, `modNetwork`, `modCombat`
* Convert repeated logic into reusable `Function` or `Sub`.

## 8. SQL queries

* Always use parameterized queries (`?`).
* Always close all `Recordset` objects.

```vb
Dim RS As ADODB.Recordset
Set RS = Query("SELECT nivel FROM user WHERE id = ?;", userId)

If Not RS.EOF Then
    nivel = RS!nivel
End If

Call RS.Close
```

## 9. Localized messages

* Use `WriteLocaleMsg` or `JsonLanguage.Item("KEY")`.

```vb
Call WriteLocaleMsg(UserIndex, "1291", FONTTYPE_INFOBOLD, GOLD_PRICE)
```

## 10. Clear control flow

* Use `Exit Sub` for early exits.
* Avoid unnecessary nested structures.

```vb
If Not EstaAutenticado(UserIndex) Then
    Call Desconectar(UserIndex)
    Exit Sub
End If
```

## 11. Pure functions and no side effects

* Prefer `Function` for validations or transformations.
* Avoid modifying global variables unnecessarily.

## 12. Separation of business, network and UI logic

* Separate concerns:

  * Network logic (`modNetwork`)
  * Business rules (`modUsuario`, `modTienda`)
  * UI/output (`WriteConsoleMsg`, `WriteLocaleMsg`)

## 13. Explicit identifiers

* Use clear, specific names.
* Avoid generic names like `dato`, `res`, `temp`.

```vb
Dim creditAmount As Long
Dim connectionId As Integer
```
