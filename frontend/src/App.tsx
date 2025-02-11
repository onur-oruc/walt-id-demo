import { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, Grid, Container } from '@mui/material';
import { getAllDids, getAllCredentials } from './services/api';

function App() {
  const [dids, setDids] = useState<any[]>([]);
  const [credentials, setCredentials] = useState<any[]>([]);
  const [selectedDid, setSelectedDid] = useState<string | null>(null);
  const walletId = import.meta.env.VITE_OEM_WALLET_ID;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const didsData = await getAllDids();
        setDids(didsData);
        const credsData = await getAllCredentials();
        setCredentials(credsData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  const getLastComponent = (did: string) => {
    return did.split(':').pop();
  };

  const filteredCredentials = credentials.filter(
    cred => cred.parsedDocument?.credentialSubject?.id === selectedDid
  );

  return (
    <Container>
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" gutterBottom>
          OEM Wallet ID: {walletId}
        </Typography>

        <Typography variant="h5" gutterBottom>
          DIDs
        </Typography>
        <Grid container spacing={2}>
          {dids.map((did) => (
            <Grid item xs={12} sm={6} md={4} key={did.did}>
              <Card 
                onClick={() => setSelectedDid(did.did)}
                sx={{ cursor: 'pointer', bgcolor: selectedDid === did.did ? '#e3f2fd' : 'white' }}
              >
                <CardContent>
                  <Typography>DID: {did.did}</Typography>
                  <Typography>Internal ID: {getLastComponent(did.did)}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {selectedDid && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom>
              Credentials for {selectedDid}
            </Typography>
            <Grid container spacing={2}>
              {filteredCredentials.map((cred, index) => (
                <Grid item xs={12} key={index}>
                  <Card>
                    <CardContent>
                      <pre>{JSON.stringify(cred, null, 2)}</pre>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default App;
