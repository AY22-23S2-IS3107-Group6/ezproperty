import { Box, SimpleGrid } from "@chakra-ui/react";

const Form = (props) => {
  return (
    <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
      <SimpleGrid
        columns={{ base: 1, md: 2, lg: 3, "2xl": 6 }}
        gap="20px"
        mb="20px"
      >
        Form
      </SimpleGrid>
    </Box>
  );
};

export default Form;
