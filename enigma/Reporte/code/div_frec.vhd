library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity div_frec is
    Port ( clk : in std_logic;
           div_clk : out std_logic);
end div_frec;

architecture Behavioral of div_frec is
begin
    process (clk)
        variable cuenta: std_logic_vector (27 downto 0):=X"0000000";
    begin
        if rising_edge (clk) then
            if cuenta = X"2FAF080" then -- 50 M de incrementos hacen 1 segundo
                cuenta:= X"0000000";
            else
                cuenta:= cuenta+1;
            end if;
        end if;
        div_clk <= cuenta(24);
    end process;
end Behavioral;