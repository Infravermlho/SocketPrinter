-- Documentação do componente de impressora https://ocdoc.cil.li/block:3d_printer
local component = require("component")
local printer = component.printer3d

-- Documentação do API de internet https://ocdoc.cil.li/api:internet
local net = require("internet")
local con = net.open("127.0.0.1", 50343)

-- Marca o tempo de timeout aguardando por um newline
con:setTimeout(5)

-- FUNÇÃO DE SPLIT PUXADA DO https://stackoverflow.com/questions/40149617/split-string-with-specified-delimiter-in-lua
-- split("a,b,c", ",") => {"a", "b", "c"}
function split(s, sep)
    local fields = {}
    
    local sep = sep or " "
    local pattern = string.format("([^%s]+)", sep)
    string.gsub(s, pattern, function(c) fields[#fields + 1] = c end)
    
    return fields
end

-- Executa se conectado
function connected ()
  local line = ''
  printer.reset()

  line = con:read()
  
  print("Imprimindo " .. line)
  printer.setLabel(line)
  local label = line

  line = con:read()
  printer.setTooltip(line)

  line = ''
  while (true) do
    line = con:read()      
    if (line == "END:") then
      printer.commit(1)
      break
    end

    local sha = split(line, ",")
    
    for convert = 1, 6 do 
      sha[convert] = tonumber(sha[convert])
    end

    printer.addShape(sha[1], sha[2], sha[3], sha[4], sha[5], sha[6], sha[7])
 
  end  

  local a
  local progress = "0"
  while (printer.status() == "busy") do
    print("Progresso: " .. progress .. "%")
    a, progress = printer.status()
  end 

  print("Impressão de " .. label .. " concluida!")
end


-- Parte que verifica se a conexão foi estabelecida
if (con) then
  local line = ''

  print("Tentando encontrar algum pedido...")
  line = con:read()

  if (line == "CONNECT:") then
    print("Conexão estabelecida com sucesso!")
    connected()
  else
    print("Conexão falhou...")
    print("Script encerrada.")
  end
else
  print("Conexão falhou...")
  print("Script encerrada.")
end

con:close()
