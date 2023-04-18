import React from 'react'

// Chakra imports
import { Box, SimpleGrid, Flex, Text, useColorModeValue } from "@chakra-ui/react";
import BarChart from "views/admin/dataTables/components/BarChart";
import LineChart from "views/admin/dataTables/components/LineChart";

// Custom components
import Card from "components/card/Card.js";

export default function ApartmentChart(props) {
  const { ...rest } = props;

  // Chakra Color Mode
  const textColor = useColorModeValue("secondaryGray.900", "white");
  return (
    <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
      <Card align='center' direction='column' w='100%' {...rest}>
        <Flex justify='space-between' align='start' px='10px' pt='5px'>
          <Flex flexDirection='column' align='start' me='20px'>
            <Flex align='end'>
              <Text
                color={textColor}
                fontSize='34px'
                fontWeight='700'
                lineHeight='100%'>
                Average Resale Prices over Time
              </Text>
            </Flex>
          </Flex>
        </Flex>
        <Flex justify='space-between' align='start' px='10px' pt='5px'>
          <Flex flexDirection='column' align='start' me='20px'>
            <Flex align='end'>
              <Text
                color={textColor}
                fontSize='16px'
                fontWeight= '300'
                lineHeight='150%'>
                For Apartments
              </Text>
            </Flex>
          </Flex>
        </Flex>
        <SimpleGrid
          mb="10px"
        ></SimpleGrid>
        <Box h='290px' mt='auto'>
          <LineChart />
        </Box>
      </Card>
      <SimpleGrid
          mb="20px"
        ></SimpleGrid>
      <Card align='center' direction='column' w='100%' {...rest}>
        <Flex justify='space-between' align='start' px='10px' pt='5px'>
          <Flex flexDirection='column' align='start' me='20px'>
            <Flex align='end'>
              <Text
                color={textColor}
                fontSize='34px'
                fontWeight='700'
                lineHeight='100%'>
                Highest Average Resale Price by District
              </Text>
            </Flex>
          </Flex>
        </Flex>
        <Flex justify='space-between' align='start' px='10px' pt='5px'>
          <Flex flexDirection='column' align='start' me='20px'>
            <Flex align='end'>
              <Text
                color={textColor}
                fontSize='16px'
                fontWeight= '300'
                lineHeight='150%'>
                For Apartments
              </Text>
            </Flex>
          </Flex>
        </Flex>
        <SimpleGrid
          mb="10px"
        ></SimpleGrid>
        <Box h='290px' mt='auto'>
          <BarChart />
        </Box>
      </Card>
    </Box>
  );
}