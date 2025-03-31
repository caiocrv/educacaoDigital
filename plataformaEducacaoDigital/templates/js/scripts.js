function validarSenha(event) {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    
    // Medir o tamanho da senha
    var character = password.length
    
    // Validando senha
    var characterSpecial = 0
    var characterUpper = 0
    var qtdCharacter = 0

    console.log("VERIFICANDO SENHA");
    if (password == confirmPassword) 
    {
        console.log("VERIFICANDO NÍVEL DA SENHA");
        for (var i = 0; character <= i; i += 1) 
        {
            alert(password[i]);
            qtdCharacter += 1
            if (password.charAt(i) === ' ')
            {
                alert("⚠️ Senha não pode conter espaço.");
                event.preventDefult();
                return false
            }
            else if (password[i] == "@" || password[i] == "#" || password[i] == "?" || password[i] == "!" || password[i] == "&") {
                characterSpecial += 1;
            }
            else if (password[i] === password[i].toUpperCase())
            {
                characterUpper += 1;
            }
        } 

        if (characterSpecial < 1) 
        {
            alert("⚠️ Senha não contém nenhum caractere especial. Tente utilizar @, #, ?, ! ou &.")
            event.preventDefult();
            return false
        }
        else if (qtdCharacter < 6)  
        {
            alert("⚠️ Senha não contém quantidade mínima de caracteres.")
            event.preventDefault();
            return false
        }
        else if (characterUpper < 1)
        {
            alert("⚠️ Senha não contém letra maiúscula.")
            event.preventDefault();
            return false
        }
        else
        {
            alert("Usuário cadastrado")
        }
    }
    else{
        alert("⚠️ As senhas não coincidem! Por favor, digite novamente.");
        event.preventDefault();
        return false;
    }
    
}